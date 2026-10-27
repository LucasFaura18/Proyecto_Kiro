"""Filtros y tags personalizados para CineTrack.

Uso en templates: {% load watchlist_tags %}
"""

from django import template

register = template.Library()


@register.filter(name="in_set")
def in_set(value, collection) -> bool:
    """Devuelve True si ``value`` está en ``collection``.

    Permite usar ``{% if result.tmdb_id|in_set:existing_ids %}`` en templates,
    ya que Django no expone el operador ``in`` directamente sobre sets/listas
    pasados desde el contexto.

    Ejemplo::

        {% load watchlist_tags %}
        {% if result.tmdb_id|in_set:existing_ids %}
          <span>Ya en tu lista</span>
        {% endif %}
    """
    try:
        return value in collection
    except TypeError:
        return False
