"""Capa de servicios de CineTrack.

Contiene la lógica de negocio que no pertenece al modelo:

Funciones existentes (v1.0):
- ``get_next_status()``: avance de estado según la secuencia definida.
- ``get_filtered_titles()``: queryset filtrado por género y/o estado.

Funciones nuevas (v1.2 — integración TMDB):
- ``search_tmdb()``: llama a la API de TMDB y devuelve resultados normalizados.
- ``add_from_tmdb()``: crea un Title desde datos TMDB, evitando duplicados.
- ``map_tmdb_genre()``: mapea los IDs de género TMDB a GENRE_CHOICES.
- ``DuplicateTitleError``: excepción para títulos ya existentes en la watchlist.

Las vistas (views.py) deben usar estas funciones y nunca consultar el modelo
directamente, para mantener la lógica de negocio aislada (ver
``.kiro/steering/conventions.md``).
"""

from __future__ import annotations

import logging
from typing import Any

import requests
from django.conf import settings
from django.db.models import QuerySet

from watchlist.models import STATUS_ORDER, Title

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes TMDB
# ---------------------------------------------------------------------------

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Mapeo de IDs de género TMDB → clave de GENRE_CHOICES.
# Fuente: https://developer.themoviedb.org/reference/genre-movie-list
_TMDB_GENRE_MAP: dict[int, str] = {
    # Acción / Aventura / Action & Adventure (TV)
    28: "action",
    12: "action",
    10759: "action",
    # Comedia
    35: "comedy",
    # Drama / Soap
    18: "drama",
    10766: "drama",
    # Terror / Misterio
    27: "horror",
    9648: "horror",
    # Ciencia Ficción / Sci-Fi & Fantasy (TV)
    878: "scifi",
    10765: "scifi",
    # Documental
    99: "documentary",
    # Animación
    16: "animation",
    # Thriller / Crimen
    53: "thriller",
    80: "thriller",
    # Romance
    10749: "romance",
}


# ---------------------------------------------------------------------------
# Excepción de negocio
# ---------------------------------------------------------------------------


class DuplicateTitleError(Exception):
    """Se lanza cuando se intenta añadir un título cuyo tmdb_id ya existe."""

    def __init__(self, title: Title) -> None:
        self.title = title
        super().__init__(f"El título con tmdb_id={title.tmdb_id} ya existe en la watchlist.")


# ---------------------------------------------------------------------------
# Funciones existentes (v1.0) — no modificadas
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Funciones nuevas (v1.2) — integración TMDB
# ---------------------------------------------------------------------------


def map_tmdb_genre(genre_ids: list[int]) -> str:
    """Convierte una lista de IDs de género TMDB al primer género coincidente.

    Recorre ``genre_ids`` en orden y devuelve la clave de ``GENRE_CHOICES``
    correspondiente al primer ID reconocido. Si ninguno coincide, devuelve
    ``"other"``.

    Args:
        genre_ids: Lista de IDs de género devuelta por TMDB.

    Returns:
        Clave de ``GENRE_CHOICES`` (p. ej. ``"action"``).
    """
    for gid in genre_ids:
        genre = _TMDB_GENRE_MAP.get(gid)
        if genre:
            return genre
    return "other"


def search_tmdb(query: str) -> list[dict[str, Any]]:
    """Busca películas y series en TMDB por nombre.

    Llama al endpoint ``/search/multi`` de la API de TMDB con autenticación
    Bearer. Filtra los resultados a tipos ``movie`` y ``tv``, y normaliza cada
    resultado al diccionario que las vistas y plantillas esperan.

    En caso de error de red o de la API, registra el error y devuelve una
    lista vacía para no interrumpir las demás funcionalidades (AC-07.3).

    Args:
        query: Término de búsqueda proporcionado por el usuario.

    Returns:
        Lista de diccionarios con las claves:
        ``tmdb_id``, ``media_type``, ``title``, ``year``, ``genre``,
        ``synopsis``, ``poster_url``.
    """
    token = settings.TMDB_API_READ_TOKEN
    if not token:
        logger.error("TMDB_API_READ_TOKEN no está configurado en .env")
        return []

    url = f"{TMDB_BASE_URL}/search/multi"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
    }
    params: dict[str, Any] = {
        "query": query,
        "include_adult": "false",
        "language": "es-ES",
        "page": 1,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=8)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Timeout al conectar con TMDB (query=%s)", query)
        return []
    except requests.exceptions.RequestException as exc:
        logger.error("Error al llamar a TMDB: %s (query=%s)", exc, query)
        return []

    data = response.json()
    results: list[dict[str, Any]] = []

    for item in data.get("results", []):
        media_type = item.get("media_type")
        if media_type not in ("movie", "tv"):
            # Ignorar personas y otros tipos no relevantes
            continue

        # Título según el tipo de medio
        title = item.get("title") or item.get("name") or ""
        if not title:
            continue

        # Año de estreno/primera emisión
        date_str = item.get("release_date") or item.get("first_air_date") or ""
        year: int | None = None
        if date_str and len(date_str) >= 4:
            try:
                year = int(date_str[:4])
            except ValueError:
                year = None

        # Género mapeado
        genre_ids: list[int] = item.get("genre_ids") or []
        genre = map_tmdb_genre(genre_ids)

        # Sinopsis
        synopsis: str = item.get("overview") or ""

        # URL del póster
        poster_path: str = item.get("poster_path") or ""
        poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else ""

        results.append(
            {
                "tmdb_id": item.get("id"),
                "media_type": media_type,
                "title": title,
                "year": year,
                "genre": genre,
                "synopsis": synopsis,
                "poster_url": poster_url,
            }
        )

    return results


def add_from_tmdb(
    tmdb_id: int,
    media_type: str,
    title: str,
    year: int | None,
    genre: str,
    synopsis: str,
    poster_url: str,
) -> Title:
    """Crea un ``Title`` a partir de datos importados de TMDB.

    Comprueba primero si ya existe un título con el mismo ``tmdb_id``.
    Si existe, lanza ``DuplicateTitleError`` en lugar de crear un duplicado
    (AC-07.5).

    Args:
        tmdb_id: Identificador del título en TMDB.
        media_type: ``"movie"`` o ``"tv"`` (se convierte a ``"series"``).
        title: Nombre del título.
        year: Año de estreno (puede ser ``None``).
        genre: Clave de ``GENRE_CHOICES`` ya mapeada.
        synopsis: Sinopsis corta de TMDB.
        poster_url: URL del póster de TMDB.

    Returns:
        El objeto ``Title`` recién creado.

    Raises:
        DuplicateTitleError: Si ya existe un título con el mismo ``tmdb_id``.
    """
    # Comprobar duplicado
    existing = Title.objects.filter(tmdb_id=tmdb_id).first()
    if existing:
        raise DuplicateTitleError(existing)

    # Convertir media_type de TMDB a choices del modelo
    title_type = "movie" if media_type == "movie" else "series"

    return Title.objects.create(
        name=title,
        title_type=title_type,
        genre=genre,
        year=year,
        status="pending",
        synopsis=synopsis,
        poster_url=poster_url,
        tmdb_id=tmdb_id,
    )
