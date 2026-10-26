"""URLs de la app watchlist.

Tabla de rutas según design.md:

    /                 title-list     TitleListView
    /add/             title-create   TitleCreateView
    /<id>/edit/       title-update   TitleUpdateView
    /<id>/delete/     title-delete   TitleDeleteView
    /<id>/status/     title-status   TitleStatusUpdateView
"""

from django.urls import path

from watchlist import views

urlpatterns = [
    path("", views.TitleListView.as_view(), name="title-list"),
    path("add/", views.TitleCreateView.as_view(), name="title-create"),
    path("<int:pk>/edit/", views.TitleUpdateView.as_view(), name="title-update"),
    path("<int:pk>/delete/", views.TitleDeleteView.as_view(), name="title-delete"),
    path("<int:pk>/status/", views.TitleStatusUpdateView.as_view(), name="title-status"),
]
