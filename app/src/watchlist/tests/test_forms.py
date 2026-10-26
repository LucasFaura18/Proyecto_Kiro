"""Tests del formulario ``TitleForm`` (T-11.2)."""

import datetime

from watchlist.forms import TitleForm


def _base_data(**overrides):
    data = {
        "name": "Inception",
        "title_type": "movie",
        "genre": "scifi",
        "year": 2010,
        "status": "watched",
        "rating": 5,
        "notes": "",
    }
    data.update(overrides)
    return data


def test_titleform_valid_data_is_valid():
    """Datos válidos pasan la validación."""
    form = TitleForm(data=_base_data())
    assert form.is_valid(), form.errors


def test_titleform_clears_rating_when_status_not_watched():
    """Si status != watched, rating se limpia a None aunque venga relleno."""
    form = TitleForm(data=_base_data(status="pending", rating=5))
    assert form.is_valid(), form.errors
    assert form.cleaned_data["rating"] is None


def test_titleform_keeps_rating_when_watched():
    """Si status == watched, rating se conserva."""
    form = TitleForm(data=_base_data(status="watched", rating=4))
    assert form.is_valid(), form.errors
    assert form.cleaned_data["rating"] == 4


def test_titleform_requires_name():
    """El título es obligatorio (AC-01.2)."""
    form = TitleForm(data=_base_data(name=""))
    assert not form.is_valid()
    assert "name" in form.errors


def test_titleform_rejects_year_too_old():
    """Año anterior a 1888 no es válido."""
    form = TitleForm(data=_base_data(year=1800))
    assert not form.is_valid()
    assert "year" in form.errors


def test_titleform_rejects_year_too_far_future():
    """Año muy futuro (actual + 10) no es válido."""
    far_future = datetime.date.today().year + 10
    form = TitleForm(data=_base_data(year=far_future))
    assert not form.is_valid()
    assert "year" in form.errors


def test_titleform_accepts_blank_year():
    """El año es opcional."""
    form = TitleForm(data=_base_data(year="", status="pending", rating=""))
    assert form.is_valid(), form.errors
    assert form.cleaned_data["year"] is None
