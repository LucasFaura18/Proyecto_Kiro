"""Tests de la capa de servicios (T-11.1 y T-11.3)."""

from datetime import timedelta

import pytest
from django.utils import timezone

from watchlist.models import Title
from watchlist.services import get_filtered_titles, get_next_status


def test_get_next_status_sequence():
    """``get_next_status`` avanza por la secuencia correcta."""
    assert get_next_status("pending") == "watching"
    assert get_next_status("watching") == "watched"
    # En el último estado se mantiene.
    assert get_next_status("watched") == "watched"


def test_get_next_status_invalid_returns_first():
    """Un estado no válido devuelve ``pending``."""
    assert get_next_status("desconocido") == "pending"


@pytest.mark.django_db
def test_get_filtered_titles_no_filter_returns_all():
    """Sin filtros devuelve todos los títulos."""
    Title.objects.create(name="A", title_type="movie", genre="drama")
    Title.objects.create(name="B", title_type="series", genre="action")
    assert get_filtered_titles().count() == 2


@pytest.mark.django_db
def test_get_filtered_titles_by_genre():
    """Filtra solo por género."""
    Title.objects.create(name="A", title_type="movie", genre="drama")
    Title.objects.create(name="B", title_type="series", genre="action")
    result = list(get_filtered_titles(genre="action").values_list("name", flat=True))
    assert result == ["B"]


@pytest.mark.django_db
def test_get_filtered_titles_by_status():
    """Filtra solo por estado."""
    Title.objects.create(name="A", title_type="movie", genre="drama", status="watched")
    Title.objects.create(
        name="B", title_type="series", genre="action", status="pending"
    )
    result = list(get_filtered_titles(status="watched").values_list("name", flat=True))
    assert result == ["A"]


@pytest.mark.django_db
def test_get_filtered_titles_combined_genre_and_status():
    """Combina filtro de género y estado a la vez (AC-04.4)."""
    Title.objects.create(name="A", title_type="movie", genre="drama", status="watched")
    Title.objects.create(name="B", title_type="movie", genre="drama", status="pending")
    Title.objects.create(name="C", title_type="series", genre="drama", status="watched")
    result = list(
        get_filtered_titles(genre="drama", status="watched").values_list(
            "name", flat=True
        )
    )
    # Ambos filtros se aplican a la vez: A y C (drama + vistos) entran;
    # B (drama pero pendiente) queda excluido por el filtro de estado.
    assert set(result) == {"A", "C"}
    assert "B" not in result


@pytest.mark.django_db
def test_get_filtered_titles_ordered_by_created_at_desc():
    """El orden es por ``created_at`` descendente (más recientes primero)."""
    first = Title.objects.create(name="Viejo", title_type="movie", genre="drama")
    Title.objects.create(name="Nuevo", title_type="movie", genre="drama")
    # Forzamos que el primero sea más antiguo de forma determinista.
    Title.objects.filter(pk=first.pk).update(
        created_at=timezone.now() - timedelta(hours=1)
    )
    result = list(get_filtered_titles().values_list("name", flat=True))
    assert result == ["Nuevo", "Viejo"]
