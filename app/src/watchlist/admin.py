"""Configuración del sitio de administración de Django para ``watchlist``."""

from __future__ import annotations

from django.contrib import admin

from watchlist.models import Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Configuración de listado del modelo ``Title`` en el admin."""

    list_display = (
        "name",
        "title_type",
        "genre",
        "year",
        "status",
        "rating",
        "created_at",
    )
    list_filter = ("status", "genre", "title_type")
    search_fields = ("name",)
    ordering = ("-created_at",)
