"""URLs de la app watchlist.

Tabla de rutas:

    /                 title-list     TitleListView
    /add/             title-create   TitleCreateView  (solo admin/acceso directo)
    /<id>/            title-detail   TitleDetailView
    /<id>/edit/       title-update   TitleUpdateView
    /<id>/delete/     title-delete   TitleDeleteView
    /<id>/status/     title-status   TitleStatusUpdateView
    /search/          tmdb-search    TmdbSearchView   ← punto de entrada principal para añadir
    /search/add/      tmdb-add       TmdbAddView
"""

from django.urls import path

from watchlist import views

urlpatterns = [
    path("", views.TitleListView.as_view(), name="title-list"),
    path("add/", views.TitleCreateView.as_view(), name="title-create"),
    path("<int:pk>/", views.TitleDetailView.as_view(), name="title-detail"),
    path("<int:pk>/edit/", views.TitleUpdateView.as_view(), name="title-update"),
    path("<int:pk>/delete/", views.TitleDeleteView.as_view(), name="title-delete"),
    path("<int:pk>/status/", views.TitleStatusUpdateView.as_view(), name="title-status"),
    # TMDB (v1.2)
    path("search/", views.TmdbSearchView.as_view(), name="tmdb-search"),
    path("search/add/", views.TmdbAddView.as_view(), name="tmdb-add"),
]
