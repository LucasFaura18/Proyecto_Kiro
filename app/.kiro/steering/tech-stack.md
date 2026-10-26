# Stack Tecnológico — CineTrack

## Backend
- **Python** 3.11+
- **Django** 4.2 LTS
- **SQLite** (desarrollo) — fichero `db.sqlite3` en la raíz del proyecto
- **django-environ** 0.11+ — gestión de variables de entorno

## Frontend
- **Django Templates** — motor de plantillas nativo
- **Bootstrap** 5.3 (CDN) — estilos y componentes responsive
- **Font Awesome** 6 (CDN) — iconografía (estrellas de puntuación, plataformas)
- Sin frameworks JavaScript adicionales (vanilla JS para interacciones mínimas)

## Herramientas de desarrollo
- **pip** para gestión de dependencias
- **virtualenv** para entorno virtual
- **pytest-django** para tests
- **flake8** para linting
- **black** para formateo automático de código

## Estructura de dependencias (`requirements.txt`)
```
Django==4.2.16
django-environ==0.11.2
pytest==7.4.4
pytest-django==4.7.0
flake8==7.0.0
black==24.1.1
```

## Estructura de la aplicación Django
```
src/
├── manage.py
├── .env
├── requirements.txt
├── config/               ← Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── watchlist/            ← App principal
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── services.py
    ├── admin.py
    ├── templates/
    │   └── watchlist/
    │       ├── base.html
    │       ├── home.html
    │       ├── movie_list.html
    │       ├── movie_detail.html
    │       ├── movie_form.html
    │       └── movie_confirm_delete.html
    └── tests/
        └── test_models.py
```

## Decisiones de diseño
- Aplicación de una sola página principal con lista filtrable
- Sin autenticación en el MVP (lista única, sin usuarios)
- Puntuación del 1 al 5 (representada con estrellas en el frontend)
- Géneros predefinidos como choices en el modelo (no tabla separada)
- Estado de visionado: Pendiente / Viendo / Visto
