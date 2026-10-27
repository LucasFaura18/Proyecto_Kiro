"""
seed.py — Carga datos de ejemplo en la base de datos de CineTrack.

Uso:
    python seed.py

Ejecutar desde app/src/ con el entorno virtual activado.
El script borra los títulos existentes antes de insertar los nuevos.
"""

import os
import sys
from pathlib import Path
import django

# ---------------------------------------------------------------------------
# Bootstrap de Django
# ---------------------------------------------------------------------------
# Asegurarse de que src/ está en el path y el .env está cargado
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Cargar el .env manualmente antes de django.setup() para que settings.py
# encuentre SECRET_KEY aunque se ejecute fuera del servidor de desarrollo
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# ---------------------------------------------------------------------------
# Importar el modelo DESPUÉS de django.setup()
# ---------------------------------------------------------------------------
from watchlist.models import Title  # noqa: E402

# ---------------------------------------------------------------------------
# Datos de ejemplo
# ---------------------------------------------------------------------------
TITLES = [
    # --- Vistas con puntuación ---
    {
        "name": "Inception",
        "title_type": "movie",
        "genre": "scifi",
        "year": 2010,
        "status": "watched",
        "rating": 5,
        "notes": "Una de las mejores películas de Nolan. El final sigue dando que hablar.",
    },
    {
        "name": "Breaking Bad",
        "title_type": "series",
        "genre": "thriller",
        "year": 2008,
        "status": "watched",
        "rating": 5,
        "notes": "Imprescindible. Walter White es uno de los mejores personajes de la TV.",
    },
    {
        "name": "Interstellar",
        "title_type": "movie",
        "genre": "scifi",
        "year": 2014,
        "status": "watched",
        "rating": 4,
        "notes": "Visualmente impresionante. La banda sonora de Zimmer es brutal.",
    },
    {
        "name": "El Padrino",
        "title_type": "movie",
        "genre": "drama",
        "year": 1972,
        "status": "watched",
        "rating": 5,
        "notes": "Clásico absoluto. Hay que verla al menos una vez.",
    },
    {
        "name": "Chernobyl",
        "title_type": "series",
        "genre": "drama",
        "year": 2019,
        "status": "watched",
        "rating": 5,
        "notes": "Miniserie devastadora. Perfecta en todos los sentidos.",
    },
    {
        "name": "The Office (US)",
        "title_type": "series",
        "genre": "comedy",
        "year": 2005,
        "status": "watched",
        "rating": 4,
        "notes": "Perfecta para ver sin pensar. Michael Scott es un genio.",
    },
    {
        "name": "Parásitos",
        "title_type": "movie",
        "genre": "thriller",
        "year": 2019,
        "status": "watched",
        "rating": 5,
        "notes": "Bong Joon-ho a un nivel diferente. No leer nada antes de verla.",
    },
    {
        "name": "Toy Story",
        "title_type": "movie",
        "genre": "animation",
        "year": 1995,
        "status": "watched",
        "rating": 4,
        "notes": "Un clásico que aguanta perfectamente el paso del tiempo.",
    },
    # --- Viendo ahora ---
    {
        "name": "The Last of Us",
        "title_type": "series",
        "genre": "drama",
        "year": 2023,
        "status": "watching",
        "rating": None,
        "notes": "Por el capítulo 5. Muy buena adaptación del videojuego.",
    },
    {
        "name": "Dune: Parte Dos",
        "title_type": "movie",
        "genre": "scifi",
        "year": 2024,
        "status": "watching",
        "rating": None,
        "notes": "A medias. Las escenas de Arrakis son una pasada visualmente.",
    },
    {
        "name": "Shogun",
        "title_type": "series",
        "genre": "drama",
        "year": 2024,
        "status": "watching",
        "rating": None,
        "notes": "Empezada hace poco. Gran ambientación feudal japonesa.",
    },
    # --- Pendientes ---
    {
        "name": "Oppenheimer",
        "title_type": "movie",
        "genre": "drama",
        "year": 2023,
        "status": "pending",
        "rating": None,
        "notes": "Pendiente desde el estreno. Dicen que hay que verla en IMAX.",
    },
    {
        "name": "True Detective",
        "title_type": "series",
        "genre": "thriller",
        "year": 2014,
        "status": "pending",
        "rating": None,
        "notes": "Me la han recomendado varias veces. Primera temporada dicen que es la mejor.",
    },
    {
        "name": "Annihilation",
        "title_type": "movie",
        "genre": "scifi",
        "year": 2018,
        "status": "pending",
        "rating": None,
        "notes": "",
    },
    {
        "name": "Succession",
        "title_type": "series",
        "genre": "drama",
        "year": 2018,
        "status": "pending",
        "rating": None,
        "notes": "Todo el mundo habla de ella. Pendiente de sacar tiempo.",
    },
    {
        "name": "Alien: Romulus",
        "title_type": "movie",
        "genre": "horror",
        "year": 2024,
        "status": "pending",
        "rating": None,
        "notes": "",
    },
    {
        "name": "Planeta Tierra II",
        "title_type": "series",
        "genre": "documentary",
        "year": 2016,
        "status": "pending",
        "rating": None,
        "notes": "Documental de la BBC. Para ver con calma.",
    },
    {
        "name": "Everything Everywhere All at Once",
        "title_type": "movie",
        "genre": "action",
        "year": 2022,
        "status": "pending",
        "rating": None,
        "notes": "Ganó el Oscar. Dicen que es una locura en el buen sentido.",
    },
]

# ---------------------------------------------------------------------------
# Inserción
# ---------------------------------------------------------------------------
def run():
    existing = Title.objects.count()
    if existing:
        print(f"⚠️  Se borrarán {existing} título(s) existente(s).")
        Title.objects.all().delete()

    titles = [Title(**data) for data in TITLES]
    Title.objects.bulk_create(titles)

    print(f"✅ {len(titles)} títulos insertados:")
    watched  = sum(1 for t in TITLES if t["status"] == "watched")
    watching = sum(1 for t in TITLES if t["status"] == "watching")
    pending  = sum(1 for t in TITLES if t["status"] == "pending")
    print(f"   • Vistos:     {watched}")
    print(f"   • Viendo:     {watching}")
    print(f"   • Pendientes: {pending}")


if __name__ == "__main__":
    run()
