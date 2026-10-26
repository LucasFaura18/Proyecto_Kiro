"""Formularios de CineTrack.

``TitleForm`` es un ``ModelForm`` sobre ``Title`` con:

- Todos los campos del diseño, con widgets Bootstrap 5
  (``form-control`` / ``form-select``) para que las plantillas (Parte B)
  los rendericen sin tocar el formulario.
- Validación en ``clean()``: la puntuación se limpia a ``None`` si
  ``status != "watched"`` (AC-01.4 y AC-03.3).
- Validación de ``year`` entre 1888 y el año actual + 2.
"""

from __future__ import annotations

import datetime

from django import forms
from django.core.exceptions import ValidationError

from watchlist.models import Title


class TitleForm(forms.ModelForm):
    """``ModelForm`` para crear y editar títulos."""

    class Meta:
        model = Title
        fields = [
            "name",
            "title_type",
            "genre",
            "year",
            "status",
            "rating",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "title_type": forms.Select(attrs={"class": "form-select"}),
            "genre": forms.Select(attrs={"class": "form-select"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 5}
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean(self) -> dict:
        """Limpia el formulario.

        Si el estado no es ``"watched"``, la puntuación se ignora (se pone a
        ``None``) aunque el usuario la haya rellenado, según AC-01.4 y AC-03.3.
        """
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        rating = cleaned_data.get("rating")
        if status != "watched" and rating is not None:
            cleaned_data["rating"] = None
        return cleaned_data

    def clean_year(self) -> int | None:
        """Valida que el año esté entre 1888 y el año actual + 2."""
        year = self.cleaned_data.get("year")
        if year is None:
            return year
        current_year = datetime.date.today().year
        if year < 1888 or year > current_year + 2:
            raise ValidationError(f"El año debe estar entre 1888 y {current_year + 2}.")
        return year
