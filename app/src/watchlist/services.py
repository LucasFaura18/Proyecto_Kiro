"""Capa de servicios de CineTrack.

Contiene la lógica de negocio que no pertenece al modelo:

- ``get_next_status()``: avance de estado según la secuencia definida.
- ``get_filtered_titles()``: queryset filtrado por género y/o estado.

Las vistas (Parte B) deben usar estas funciones y nunca consultar el modelo
directamente, para mantener la lógica de negocio aislada (ver
``.kiro/steering/conventions.md``).
"""

from __future__ import annotations

from django.db.models import QuerySet

from watchlist.models import STATUS_ORDER, Title


def get_next_status(current: str) -> str:
    """Devuelve el siguiente estado en la secuencia pendiente -> viendo -> visto.

    Args:
        current: Estado actual (``"pending"``, ``"watching"`` o ``"watched"``).

    Returns:
        El siguiente estado. Si ``current`` es ``"watched"`` (último) se
        mantiene. Si ``current`` no es válido, devuelve ``"pending"``.
    """
    try:
        index = STATUS_ORDER.index(current)
    except ValueError:
        return STATUS_ORDER[0]
    if index < len(STATUS_ORDER) - 1:
        return STATUS_ORDER[index + 1]
    return current


def get_filtered_titles(
    genre: str | None = None, status: str | None = None
) -> QuerySet[Title]:
    """Devuelve títulos filtrados por género y/o estado, los recientes primero.

    Args:
        genre: Género a filtrar (clave de ``GENRE_CHOICES``). ``None`` = sin
            filtro.
        status: Estado a filtrar (clave de ``STATUS_CHOICES``). ``None`` = sin
            filtro.

    Returns:
        QuerySet ordenado por ``created_at`` descendente (más recientes
        primero).
    """
    queryset = Title.objects.all()
    if genre:
        queryset = queryset.filter(genre=genre)
    if status:
        queryset = queryset.filter(status=status)
    return queryset.order_by("-created_at")
