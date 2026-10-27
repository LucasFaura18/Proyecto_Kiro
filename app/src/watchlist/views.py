"""Vistas de CineTrack (Parte B).

Implementa las cinco CBVs del diseño usando la capa de servicios.
Las vistas nunca acceden al ORM directamente; toda consulta pasa por
``watchlist.services`` (ver ``.kiro/steering/conventions.md``).
"""

from __future__ import annotations

from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from watchlist.forms import TitleEditForm, TitleForm
from watchlist.models import GENRE_CHOICES, STATUS_CHOICES, Title
from watchlist.services import (
    DuplicateTitleError,
    add_from_tmdb,
    get_filtered_titles,
    get_next_status,
    search_tmdb,
)


class TitleListView(ListView):
    """Lista principal con filtrado opcional por género y/o estado (US-04)."""

    model = Title
    template_name = "watchlist/title_list.html"
    context_object_name = "titles"

    def get_queryset(self):
        genre = self.request.GET.get("genre") or None
        status = self.request.GET.get("status") or None
        return get_filtered_titles(genre=genre, status=status)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["genre_choices"] = GENRE_CHOICES
        ctx["status_choices"] = STATUS_CHOICES
        ctx["current_genre"] = self.request.GET.get("genre", "")
        ctx["current_status"] = self.request.GET.get("status", "")
        return ctx


class TitleCreateView(CreateView):
    """Formulario para añadir un nuevo título (US-01)."""

    model = Title
    form_class = TitleForm
    template_name = "watchlist/title_form.html"
    success_url = reverse_lazy("title-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"«{self.object.name}» se ha añadido correctamente.",
        )
        return response


class TitleUpdateView(UpdateView):
    """Formulario para editar estado, puntuación y notas de un título (US-01, US-03).

    Los campos de identidad (name, title_type, genre, year) son inmutables
    desde la UI: provienen de TMDB y se muestran como información de solo
    lectura en el template.
    """

    model = Title
    form_class = TitleEditForm
    template_name = "watchlist/title_form.html"
    success_url = reverse_lazy("title-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"«{self.object.name}» se ha actualizado correctamente.",
        )
        return response


class TitleStatusUpdateView(View):
    """Avanza el estado de un título al siguiente en la secuencia (US-02).

    Solo acepta POST para evitar cambios de estado por GET accidental.
    """

    http_method_names = ["post"]

    def post(self, request, pk):
        title = get_object_or_404(Title, pk=pk)
        new_status = get_next_status(title.status)
        title.status = new_status
        # Si el estado ya no es "watched", limpiamos la puntuación (AC-02.3)
        if new_status != "watched":
            title.rating = None
        title.save()
        messages.success(
            request,
            f"Estado de «{title.name}» actualizado a «{title.get_status_display()}».",
        )
        return redirect("title-list")

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


class TitleDeleteView(DeleteView):
    """Confirmación y borrado de un título (US-05)."""

    model = Title
    template_name = "watchlist/title_confirm_delete.html"
    success_url = reverse_lazy("title-list")

    def form_valid(self, form):
        name = self.object.name
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"«{name}» se ha eliminado correctamente.",
        )
        return response


class TitleDetailView(DetailView):
    """Vista de detalle de un título con póster y sinopsis completos."""

    model = Title
    template_name = "watchlist/title_detail.html"
    context_object_name = "title"


# ---------------------------------------------------------------------------
# Vistas TMDB (v1.2 — US-07)
# ---------------------------------------------------------------------------


class TmdbSearchView(View):
    """Formulario de búsqueda TMDB y visualización de resultados (US-07).

    GET sin parámetros → formulario vacío.
    GET con ``?q=<término>`` → llama a ``search_tmdb()`` y muestra resultados.
    """

    template_name = "watchlist/tmdb_search.html"

    def get(self, request):
        query = request.GET.get("q", "").strip()
        results: list = []
        error: str = ""

        if query:
            results = search_tmdb(query)
            if results is None:
                # search_tmdb devuelve lista vacía en caso de error de API
                results = []
                error = (
                    "No se ha podido conectar con TMDB. "
                    "Comprueba tu conexión e inténtalo de nuevo."
                )

        # Conjunto de tmdb_ids ya guardados para marcar duplicados (mejora 6)
        existing_ids: set[int] = set(
            Title.objects.filter(tmdb_id__isnull=False).values_list("tmdb_id", flat=True)
        )

        return self._render(
            request,
            query=query,
            results=results,
            error=error,
            existing_ids=existing_ids,
        )

    def _render(
        self,
        request,
        *,
        query: str,
        results: list,
        error: str,
        existing_ids: set | None = None,
    ):
        from django.shortcuts import render

        return render(
            request,
            self.template_name,
            {
                "query": query,
                "results": results,
                "error": error,
                "existing_ids": existing_ids or set(),
            },
        )


class TmdbAddView(View):
    """Añade un resultado de TMDB a la watchlist (US-07).

    Solo acepta POST. Recibe los datos del título directamente del formulario
    oculto del resultado TMDB para evitar una segunda llamada a la API.
    """

    http_method_names = ["post"]

    def post(self, request):
        # Leer datos del formulario oculto
        try:
            tmdb_id = int(request.POST.get("tmdb_id", 0))
        except (ValueError, TypeError):
            tmdb_id = 0

        media_type = request.POST.get("media_type", "movie")
        title = request.POST.get("title", "").strip()
        synopsis = request.POST.get("synopsis", "").strip()
        poster_url = request.POST.get("poster_url", "").strip()
        genre = request.POST.get("genre", "other")

        # Año: puede ser vacío
        try:
            year: int | None = int(request.POST.get("year", ""))
        except (ValueError, TypeError):
            year = None

        # Validación mínima
        if not tmdb_id or not title:
            messages.error(request, "Datos incompletos. No se ha podido añadir el título.")
            return redirect("tmdb-search")

        try:
            new_title = add_from_tmdb(
                tmdb_id=tmdb_id,
                media_type=media_type,
                title=title,
                year=year,
                genre=genre,
                synopsis=synopsis,
                poster_url=poster_url,
            )
            messages.success(
                request,
                f"«{new_title.name}» se ha añadido a tu lista correctamente.",
            )
        except DuplicateTitleError as exc:
            messages.warning(
                request,
                f"«{exc.title.name}» ya está en tu lista.",
            )

        return redirect("title-list")

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
