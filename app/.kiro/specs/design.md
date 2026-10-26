# Design — CineTrack MVP (v1.0)

> Documento de diseño técnico generado a partir de `requirements.md`  
> Stack: Python 3.11 · Django 4.2 LTS · SQLite (integrado en Django) · Bootstrap 5

---

## Arquitectura general

CineTrack sigue la arquitectura **MTV** de Django (Model – Template – View), con una capa de servicios para la lógica de negocio. La base de datos es **SQLite**, gestionada completamente por el ORM de Django — no requiere servidor externo, todo reside en un fichero `db.sqlite3` dentro del propio proyecto.

```mermaid
graph TD
    Browser["🌐 Navegador"] -->|HTTP Request| URLs["urls.py\n(enrutamiento)"]
    URLs --> Views["views.py\n(CBVs)"]
    Views --> Services["services.py\n(lógica de negocio)"]
    Services --> Models["models.py\n(ORM Django)"]
    Models --> DB[("db.sqlite3\nSQLite — gestionado por Django")]
    Views --> Templates["templates/\n(HTML + Bootstrap 5)"]
    Templates --> Browser
```

---

## Modelo de datos

### Entidad principal: `Title`

```python
class Title(models.Model):
    # Datos principales
    name        = CharField(max_length=200)           # Título obligatorio
    title_type  = CharField(choices=TYPE_CHOICES)     # "movie" | "series"
    genre       = CharField(choices=GENRE_CHOICES)    # Género predefinido
    year        = PositiveIntegerField(null=True, blank=True)

    # Estado y valoración
    status      = CharField(choices=STATUS_CHOICES, default="pending")
    rating      = PositiveSmallIntegerField(
                      null=True, blank=True,
                      validators=[MinValueValidator(1), MaxValueValidator(5)]
                  )
    # Metadatos
    notes       = TextField(blank=True)
    created_at  = DateTimeField(auto_now_add=True)
    updated_at  = DateTimeField(auto_now=True)
```

### Choices

```python
TYPE_CHOICES = [
    ("movie",   "Película"),
    ("series",  "Serie"),
]

GENRE_CHOICES = [
    ("action",       "Acción"),
    ("comedy",       "Comedia"),
    ("drama",        "Drama"),
    ("horror",       "Terror"),
    ("scifi",        "Ciencia Ficción"),
    ("documentary",  "Documental"),
    ("animation",    "Animación"),
    ("thriller",     "Thriller"),
    ("romance",      "Romance"),
    ("other",        "Otros"),
]

STATUS_CHOICES = [
    ("pending",  "Pendiente"),
    ("watching", "Viendo"),
    ("watched",  "Visto"),
]
```

### Diagrama ER — v1.0

```mermaid
erDiagram
    TITLE {
        int id PK
        string name
        string title_type
        string genre
        int year
        string status
        int rating
        text notes
        datetime created_at
        datetime updated_at
    }
```

---

## URLs y vistas (CBVs)

| URL | Nombre | View | Descripción |
|---|---|---|---|
| `/` | `title-list` | `TitleListView` | Lista con filtros por género y estado |
| `/add/` | `title-create` | `TitleCreateView` | Formulario para añadir título |
| `/<id>/edit/` | `title-update` | `TitleUpdateView` | Editar un título existente |
| `/<id>/delete/` | `title-delete` | `TitleDeleteView` | Confirmar y eliminar |
| `/<id>/status/` | `title-status` | `TitleStatusUpdateView` | Avanzar al siguiente estado |

---

## Formularios

### `TitleForm` (ModelForm)

Campos: `name`, `title_type`, `genre`, `year`, `status`, `rating`, `notes`

Validaciones en `clean()`:
- Si `status != "watched"` → limpiar `rating` a `None`
- `year` entre 1888 y año actual + 2

---

## Capa de servicios — `services.py`

```python
def get_next_status(current: str) -> str:
    """Devuelve el siguiente estado en la secuencia pending→watching→watched."""

def get_filtered_titles(genre: str | None, status: str | None) -> QuerySet:
    """QuerySet filtrado por género y/o estado, ordenado por -created_at."""
```

---

## Templates

```
templates/
├── base.html                          ← Layout raíz (navbar + Bootstrap 5)
└── watchlist/
    ├── title_list.html                ← Lista principal con barra de filtros
    ├── title_form.html                ← Crear / Editar (mismo template)
    ├── title_confirm_delete.html      ← Confirmación de borrado
    └── partials/
        ├── _title_card.html           ← Tarjeta individual de un título
        ├── _filter_bar.html           ← Selector de filtros
        └── _star_rating.html          ← Componente de estrellas (1-5)
```

### Wireframe — Lista principal

```
┌───────────────────────────────────────────────────────┐
│  🎬 CineTrack                            [+ Añadir]   │
├───────────────────────────────────────────────────────┤
│  Género: [Todos ▼]   Estado: [Todos ▼]                │
├───────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ 🎬 Título   │  │ 📺 Título   │  │ 🎬 Título   │   │
│  │ Drama · 23  │  │ Acción · 22 │  │ Terror · 21 │   │
│  │ [Pendiente] │  │ [Viendo]    │  │ [Visto]     │   │
│  │ —           │  │ —           │  │ ★★★★☆       │   │
│  │ [✏️]  [🗑️] │  │ [✏️]  [🗑️] │  │ [✏️]  [🗑️] │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└───────────────────────────────────────────────────────┘
```

---

## Flujo de datos — Añadir un título

```mermaid
sequenceDiagram
    actor U as 👤 Usuario
    participant V as TitleCreateView
    participant F as TitleForm
    participant S as services.py
    participant DB as db.sqlite3

    U->>V: GET /add/
    V->>U: Formulario vacío

    U->>V: POST /add/ (datos)
    V->>F: form.is_valid()

    alt Válido
        F->>S: Validaciones de negocio
        S->>DB: title.save()
        DB-->>V: OK
        V->>U: Redirect lista + mensaje éxito
    else Inválido
        F-->>V: Errores
        V->>U: Formulario con errores
    end
```

---

## Evolución del modelo — v1.1 (Plataformas, US-06)

```mermaid
erDiagram
    TITLE {
        int id PK
        string name
        string title_type
        string genre
        int year
        string status
        int rating
        text notes
        datetime created_at
        datetime updated_at
    }
    PLATFORM {
        int id PK
        string name
        string slug
    }
    TITLE ||--o{ TITLE_PLATFORM : "disponible en"
    PLATFORM ||--o{ TITLE_PLATFORM : "contiene"
    TITLE_PLATFORM {
        int title_id FK
        int platform_id FK
    }
```

Plataformas predefinidas: Netflix, HBO Max, Disney+, Prime Video, Movistar+, Otros.  
Se cargarán con un `data migration` al hacer `migrate`.
