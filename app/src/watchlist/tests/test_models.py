"""Tests del modelo ``Title``."""

import pytest

from watchlist.models import STATUS_ORDER, Title


@pytest.mark.django_db
def test_title_str_returns_name():
    """``__str__`` devuelve el nombre del título."""
    title = Title.objects.create(name="Inception", title_type="movie", genre="scifi")
    assert str(title) == "Inception"


@pytest.mark.django_db
def test_title_default_status_is_pending():
    """El estado por defecto es ``pending``."""
    title = Title.objects.create(name="X", title_type="movie", genre="drama")
    assert title.status == "pending"


@pytest.mark.django_db
def test_title_get_next_status_advances_sequence():
    """El método de instancia avanza por la secuencia correcta."""
    title = Title.objects.create(name="X", title_type="movie", genre="drama")
    assert title.get_next_status() == "watching"
    title.status = "watching"
    assert title.get_next_status() == "watched"
    title.status = "watched"
    # En el último estado se mantiene.
    assert title.get_next_status() == "watched"


@pytest.mark.django_db
def test_title_get_next_status_invalid_status_returns_pending():
    """Un estado no válido devuelve el primero (``pending``)."""
    title = Title.objects.create(name="X", title_type="movie", genre="drama")
    title.status = "no-valido"
    assert title.get_next_status() == "pending"


def test_status_order_constant():
    """La secuencia de estados es pendiente -> viendo -> visto."""
    assert STATUS_ORDER == ["pending", "watching", "watched"]
