"""Modelo de datos de CineTrack.

Define el modelo ``Title`` (películas y series) con sus *choices* de tipo,
género y estado de visionado. La lógica de avance de estado vive en
``services.py``; aquí solo se expone un método de conveniencia
``get_next_status()`` sobre la instancia.
"""

from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# --- Choices ---------------------------------------------------------------

TYPE_CHOICES = [
    ("movie", "Película"),
    ("series", "Serie"),
]

GENRE_CHOICES = [
    ("action", "Acción"),
    ("comedy", "Comedia"),
    ("drama", "Drama"),
    ("horror", "Terror"),
    ("scifi", "Ciencia Ficción"),
    ("documentary", "Documental"),
    ("animation", "Animación"),
    ("thriller", "Thriller"),
    ("romance", "Romance"),
    ("other", "Otros"),
]

STATUS_CHOICES = [
    ("pending", "Pendiente"),
    ("watching", "Viendo"),
    ("watched", "Visto"),
]

# Secuencia de avance de estado: Pendiente -> Viendo -> Visto.
# Fuente única de verdad para ``services.get_next_status()`` y
# ``Title.get_next_status()``.
STATUS_ORDER = ["pending", "watching", "watched"]


class Title(models.Model):
    """Título (película o serie) de la watchlist personal.

    Attributes:
        name: Nombre del título (obligatorio).
        title_type: ``"movie"`` o ``"series"``.
        genre: Género predefinido (ver ``GENRE_CHOICES``).
        year: Año de estreno (opcional).
        status: Estado de visionado (``pending``/``watching``/``watched``).
        rating: Puntuación 1-5 (solo si ``status == "watched"``).
        notes: Notas libres (opcional).
        tmdb_id: Identificador único en TMDB (null si se añadió manualmente).
        synopsis: Sinopsis corta importada de TMDB.
        poster_url: URL del póster de TMDB.
    """

    name = models.CharField(max_length=200, verbose_name="título")
    title_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, verbose_name="tipo"
    )
    genre = models.CharField(
        max_length=20, choices=GENRE_CHOICES, verbose_name="género"
    )
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name="año")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="estado",
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="puntuación",
    )
    notes = models.TextField(blank=True, verbose_name="notas")
    # --- Campos TMDB (v1.2) -----------------------------------------------
    # Identificador único en TMDB. Permite detectar duplicados (AC-07.5).
    # null/blank porque los títulos añadidos manualmente no tienen tmdb_id.
    tmdb_id = models.PositiveIntegerField(
        null=True, blank=True, unique=True, db_index=True, verbose_name="ID TMDB"
    )
    # Sinopsis corta importada de TMDB.
    synopsis = models.TextField(blank=True, verbose_name="sinopsis")
    # URL del póster devuelta por TMDB (imagen remota).
    poster_url = models.URLField(
        max_length=500, blank=True, verbose_name="URL del póster"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="actualizado")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "título"
        verbose_name_plural = "títulos"

    def __str__(self) -> str:
        """Devuelve el nombre del título."""
        return self.name

    def get_next_status(self) -> str:
        """Devuelve el siguiente estado según ``STATUS_ORDER``.

        Si el estado actual es el último (``"watched"``), se mantiene.
        Si el estado actual no es válido, devuelve el primero (``"pending"``).
        """
        try:
            index = STATUS_ORDER.index(self.status)
        except ValueError:
            return STATUS_ORDER[0]
        if index < len(STATUS_ORDER) - 1:
            return STATUS_ORDER[index + 1]
        return self.status
