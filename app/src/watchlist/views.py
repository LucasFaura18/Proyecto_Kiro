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
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from watchlist.forms import TitleForm
from watchlist.models import GENRE_CHOICES, STATUS_CHOICES, Title
from watchlist.services import get_filtered_titles, get_next_status


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
    """Formulario para editar un título existente (US-01, US-03)."""

    model = Title
    form_class = TitleForm
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
