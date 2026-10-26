"""Tests de las vistas de watchlist (T-11.4 y T-11.5)."""

import pytest
from django.urls import reverse

from watchlist.models import Title


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_title(**kwargs):
    """Crea un Title con valores por defecto sobreescribibles."""
    defaults = {
        "name": "Test Movie",
        "title_type": "movie",
        "genre": "drama",
        "status": "pending",
    }
    defaults.update(kwargs)
    return Title.objects.create(**defaults)


# ---------------------------------------------------------------------------
# T-11.4 · TitleCreateView
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_create_view_get_returns_200(client):
    """GET /add/ devuelve el formulario vacío."""
    response = client.get(reverse("title-create"))
    assert response.status_code == 200
    assert b"Añadir título" in response.content


@pytest.mark.django_db
def test_create_view_post_valid_creates_title_and_redirects(client):
    """POST válido crea el título y redirige a la lista (AC-01.1, AC-01.5)."""
    data = {
        "name": "Inception",
        "title_type": "movie",
        "genre": "scifi",
        "year": 2010,
        "status": "pending",
        "rating": "",
        "notes": "",
    }
    response = client.post(reverse("title-create"), data=data)
    assert response.status_code == 302
    assert response["Location"] == reverse("title-list")
    assert Title.objects.filter(name="Inception").exists()


@pytest.mark.django_db
def test_create_view_post_invalid_no_name_returns_form_with_errors(client):
    """POST sin nombre devuelve 200 con errores (AC-01.2)."""
    data = {
        "name": "",
        "title_type": "movie",
        "genre": "drama",
        "year": "",
        "status": "pending",
        "rating": "",
        "notes": "",
    }
    response = client.post(reverse("title-create"), data=data)
    assert response.status_code == 200
    # El formulario debe estar en el contexto con errores
    form = response.context["form"]
    assert not form.is_valid()
    assert "name" in form.errors


@pytest.mark.django_db
def test_create_view_post_invalid_year_returns_form_with_errors(client):
    """POST con año anterior a 1888 devuelve errores en el campo year."""
    data = {
        "name": "Viejo",
        "title_type": "movie",
        "genre": "drama",
        "year": 1700,
        "status": "pending",
        "rating": "",
        "notes": "",
    }
    response = client.post(reverse("title-create"), data=data)
    assert response.status_code == 200
    form = response.context["form"]
    assert "year" in form.errors


# ---------------------------------------------------------------------------
# T-11.5 · TitleStatusUpdateView
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_status_update_advances_pending_to_watching(client):
    """POST a /status/ avanza pending → watching (AC-02.1)."""
    title = _make_title(status="pending")
    response = client.post(reverse("title-status", args=[title.pk]))
    assert response.status_code == 302
    title.refresh_from_db()
    assert title.status == "watching"


@pytest.mark.django_db
def test_status_update_advances_watching_to_watched(client):
    """POST a /status/ avanza watching → watched (AC-02.1)."""
    title = _make_title(status="watching")
    client.post(reverse("title-status", args=[title.pk]))
    title.refresh_from_db()
    assert title.status == "watched"


@pytest.mark.django_db
def test_status_update_watched_stays_watched(client):
    """Un título ya visto no avanza más (AC-02.1 — clamp al final)."""
    title = _make_title(status="watched", rating=4)
    client.post(reverse("title-status", args=[title.pk]))
    title.refresh_from_db()
    assert title.status == "watched"


@pytest.mark.django_db
def test_status_update_redirects_to_list(client):
    """POST a /status/ siempre redirige a la lista principal."""
    title = _make_title(status="pending")
    response = client.post(reverse("title-status", args=[title.pk]))
    assert response.status_code == 302
    assert response["Location"] == reverse("title-list")


@pytest.mark.django_db
def test_status_update_get_not_allowed(client):
    """GET a /status/ devuelve 405 Method Not Allowed."""
    title = _make_title(status="pending")
    response = client.get(reverse("title-status", args=[title.pk]))
    assert response.status_code == 405


# ---------------------------------------------------------------------------
# TitleListView — filtros básicos
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_list_view_returns_200(client):
    """GET / devuelve 200."""
    response = client.get(reverse("title-list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_view_empty_shows_no_results_message(client):
    """Sin títulos se muestra el mensaje de lista vacía (AC-04.3)."""
    response = client.get(reverse("title-list"))
    assert b"No hay t" in response.content  # "No hay títulos en esta categoría."


@pytest.mark.django_db
def test_list_view_filter_by_genre(client):
    """Filtrar por género devuelve solo los títulos de ese género (AC-04.1)."""
    _make_title(name="Drama Movie", genre="drama")
    _make_title(name="Action Movie", genre="action")
    response = client.get(reverse("title-list") + "?genre=drama")
    titles = response.context["titles"]
    assert all(t.genre == "drama" for t in titles)
    assert titles.count() == 1


@pytest.mark.django_db
def test_list_view_filter_combined_genre_and_status(client):
    """Combinar género + estado aplica ambos filtros (AC-04.4)."""
    _make_title(name="A", genre="drama", status="watched")
    _make_title(name="B", genre="drama", status="pending")
    _make_title(name="C", genre="action", status="watched")
    response = client.get(reverse("title-list") + "?genre=drama&status=watched")
    titles = list(response.context["titles"].values_list("name", flat=True))
    assert titles == ["A"]


# ---------------------------------------------------------------------------
# TitleDeleteView
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_delete_view_get_shows_confirm_page(client):
    """GET a /delete/ muestra la página de confirmación (AC-05.1)."""
    title = _make_title()
    response = client.get(reverse("title-delete", args=[title.pk]))
    assert response.status_code == 200
    assert title.name.encode() in response.content


@pytest.mark.django_db
def test_delete_view_post_removes_title_and_redirects(client):
    """POST confirma el borrado y redirige (AC-05.2)."""
    title = _make_title()
    pk = title.pk
    response = client.post(reverse("title-delete", args=[pk]))
    assert response.status_code == 302
    assert not Title.objects.filter(pk=pk).exists()
