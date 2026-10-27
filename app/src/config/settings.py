"""
Configuración del proyecto Django para CineTrack.

Generado con 'django-admin startproject' (Django 4.2 LTS) y adaptado
segun el stack definido en .kiro/steering/tech-stack.md:
- Variables de entorno con django-environ (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- Base de datos SQLite (integrada en Django, sin servidor externo)
- Idioma espanol y zona horaria de Madrid
- Directorio de templates a nivel de proyecto (src/templates/)
"""

from pathlib import Path

import environ

# Ruta base del proyecto (carpeta src/).
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Variables de entorno (.env) -----------------------------------------
# Lee el fichero .env si existe. En produccion puede no existir y los valores
# venir de variables de entorno reales.
env = environ.Env()
environ.Env.read_env(str(BASE_DIR / ".env"))

# SECURITY WARNING: la SECRET_KEY viene de .env, nunca se hardcodea.
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: no ejecutar con DEBUG=True en produccion.
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])


# --- Aplicaciones instaladas ---------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # App principal del proyecto
    "watchlist",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Plantillas a nivel de proyecto: base.html, watchlist/ y partials/
        # (ver design.md). APP_DIRS mantiene activa la busqueda por aplicacion.
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- Base de datos --------------------------------------------------------
# SQLite: gestionada por el ORM de Django (fichero db.sqlite3 local).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --- Validacion de contrasenas -------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internacionalizacion -------------------------------------------------
LANGUAGE_CODE = "es"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_TZ = True


# --- Ficheros estaticos --------------------------------------------------
STATIC_URL = "static/"

# --- TMDB API (v1.2) -------------------------------------------------------
# Token de solo lectura (Bearer) de la API de TMDB.
# Se lee desde .env; nunca se hardcodea en el código fuente.
TMDB_API_READ_TOKEN = env("TMDB_API_READ_TOKEN", default="")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
