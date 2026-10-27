# Tasks — CineTrack MVP (v1.0)

> Lista de tareas de implementación generada a partir de `requirements.md` y `design.md`  
> Ordenadas por dependencia — cada tarea debe completarse antes de la siguiente que la referencia.

---

## Reparto entre dos personas

- **Parte A — Datos y lógica de negocio (backend)**: BLOQUE 0, BLOQUE 1, BLOQUE 2, BLOQUE 3 y tests de esa capa (T-11.1, T-11.2, T-11.3). En v1.1: T-12.1 a T-12.5.
- **Parte B — Vistas, plantillas y calidad (frontend + controlador)**: BLOQUE 4, BLOQUE 5 (T-05 a T-09), BLOQUE 6, BLOQUE 7 (T-11.4, T-11.5). En v1.1: T-12.6 a T-12.9.

**Contrato de interfaz (lo que A expone y B consume, definido en `design.md`):**

- Modelo `Title` con campos `name, title_type, genre, year, status, rating, notes, created_at, updated_at` y los choices `TYPE_CHOICES`, `GENRE_CHOICES`, `STATUS_CHOICES`.
- `watchlist.services.get_next_status(current: str) -> str`
- `watchlist.services.get_filtered_titles(genre=None, status=None) -> QuerySet[Title]`
- `watchlist.forms.TitleForm` (ModelForm) con los 7 campos y widgets Bootstrap (`form-control` / `form-select`).

---

## Leyenda de estado

| Símbolo | Significado |
|---|---|
| `[ ]` | Pendiente |
| `[x]` | Completada |
| `[-]` | En progreso |

---

## BLOQUE 0 — Inicialización del proyecto

### T-00 · Estructura y configuración base
- [x] **T-00.1** Crear entorno virtual Python (`venv`) e instalar dependencias de `requirements.txt`
- [x] **T-00.2** Crear proyecto Django `config` con `django-admin startproject`
- [x] **T-00.3** Crear app Django `watchlist` con `python manage.py startapp`
- [x] **T-00.4** Configurar `settings.py`: base de datos SQLite, templates, apps instaladas, idioma español
- [x] **T-00.5** Crear fichero `.env` con `SECRET_KEY` y `DEBUG=True`
- [x] **T-00.6** Verificar que `python manage.py runserver` arranca sin errores

---

## BLOQUE 1 — Modelo de datos (→ US-01, US-02, US-03)

### T-01 · Modelo `Title`
- [x] **T-01.1** Definir modelo `Title` en `watchlist/models.py` con todos los campos y choices del diseño
- [x] **T-01.2** Añadir método `__str__` que devuelva el nombre del título
- [x] **T-01.3** Añadir método `get_next_status()` al modelo
- [x] **T-01.4** Registrar modelo en `watchlist/admin.py` con `list_display` útil
- [x] **T-01.5** Crear y aplicar migración inicial (`makemigrations` + `migrate`)
- [ ] **T-01.6** Verificar el modelo en el admin de Django con datos de prueba

*Requisitos cubiertos: US-01 (campo base), US-02 (campo status), US-03 (campo rating)*

---

## BLOQUE 2 — Capa de servicios (→ US-02, US-04)

### T-02 · `services.py`
- [x] **T-02.1** Implementar `get_next_status(current: str) -> str` con la secuencia pending→watching→watched
- [x] **T-02.2** Implementar `get_filtered_titles(genre, status) -> QuerySet` con filtros opcionales y orden por `-created_at`

*Requisitos cubiertos: US-02 (lógica de estado), US-04 (filtrado)*

---

## BLOQUE 3 — Formularios (→ US-01, US-03)

### T-03 · `TitleForm`
- [x] **T-03.1** Crear `TitleForm(ModelForm)` en `watchlist/forms.py` con todos los campos del diseño
- [x] **T-03.2** Implementar `clean()`: limpiar `rating` si `status != "watched"`
- [x] **T-03.3** Implementar validación de `year` (1888 ≤ year ≤ año_actual + 2)
- [x] **T-03.4** Añadir widgets Bootstrap 5 a los campos del formulario (clases `form-control`, `form-select`)

*Requisitos cubiertos: US-01 (AC-01.2, AC-01.3, AC-01.4), US-03 (AC-03.1)*

---

## BLOQUE 4 — Templates base (→ todos)

### T-04 · Sistema de templates
- [ ] **T-04.1** Crear `templates/base.html` con navbar, bloque `content`, CDN de Bootstrap 5 y Font Awesome 6
- [ ] **T-04.2** Crear partial `_star_rating.html` para mostrar puntuación como estrellas
- [ ] **T-04.3** Crear partial `_filter_bar.html` con selectores de género y estado
- [ ] **T-04.4** Crear partial `_title_card.html` con datos del título, badge de estado y botones de acción

*Prerequisito para todos los bloques de vistas*

---

## BLOQUE 5 — Vistas y URLs (→ US-01 a US-05)

### T-05 · Lista principal
- [ ] **T-05.1** Implementar `TitleListView` que pase filtros GET a `get_filtered_titles()`
- [ ] **T-05.2** Crear `watchlist/title_list.html` usando los partials de T-04
- [ ] **T-05.3** Verificar que la lista muestra mensaje vacío cuando no hay resultados (AC-04.3)

*Requisitos cubiertos: US-04 (AC-04.1, AC-04.2, AC-04.3)*

### T-06 · Crear y editar título
- [ ] **T-06.1** Implementar `TitleCreateView` con redirección a `title-list` y mensaje de éxito
- [ ] **T-06.2** Implementar `TitleUpdateView` reutilizando `title_form.html`
- [ ] **T-06.3** Crear `watchlist/title_form.html` con el formulario y manejo de errores accesible
- [ ] **T-06.4** Verificar AC-01.1, AC-01.2, AC-01.5

*Requisitos cubiertos: US-01*

### T-07 · Cambio de estado
- [ ] **T-07.1** Implementar `TitleStatusUpdateView` (POST only) que llame a `get_next_status()`
- [ ] **T-07.2** Añadir botón de cambio de estado en `_title_card.html`
- [ ] **T-07.3** Verificar secuencia pending→watching→watched (AC-02.1, AC-02.2, AC-02.3, AC-02.4)

*Requisitos cubiertos: US-02*

### T-08 · Puntuación
- [ ] **T-08.1** Asegurar que el campo rating del formulario se deshabilita visualmente cuando status ≠ "watched"
- [ ] **T-08.2** Mostrar las estrellas en la tarjeta usando `_star_rating.html`
- [ ] **T-08.3** Verificar AC-03.1, AC-03.2, AC-03.3, AC-03.4

*Requisitos cubiertos: US-03*

### T-09 · Eliminar título
- [ ] **T-09.1** Implementar `TitleDeleteView` con redirección y mensaje de confirmación
- [ ] **T-09.2** Crear `title_confirm_delete.html` con botones confirmar/cancelar
- [ ] **T-09.3** Verificar AC-05.1, AC-05.2, AC-05.3

*Requisitos cubiertos: US-05*

---

## BLOQUE 6 — Requisitos no funcionales

### T-10 · Responsive y accesibilidad
- [ ] **T-10.1** Verificar que la lista principal es usable en pantalla de 375px (móvil)
- [ ] **T-10.2** Añadir atributos `aria-label` en botones de estado y eliminar
- [ ] **T-10.3** Verificar que los errores de formulario tienen `role="alert"` o similar

*Requisitos cubiertos: RNF-01, RNF-04*

---

## BLOQUE 7 — Tests

### T-11 · Tests unitarios
- [x] **T-11.1** Test de `get_next_status()`: secuencia correcta y valor inválido
- [x] **T-11.2** Test de `TitleForm.clean()`: rating se limpia cuando status ≠ "watched"
- [x] **T-11.3** Test de `get_filtered_titles()`: filtro por género, por estado, combinado y sin filtro
- [ ] **T-11.4** Test de `TitleCreateView`: POST válido crea título y redirige; POST inválido devuelve errores
- [ ] **T-11.5** Test de `TitleStatusUpdateView`: el estado avanza correctamente

---

## BLOQUE 8 — Cambio de requisitos (v1.1 · US-06)

> Este bloque se activa tras la entrega del MVP. Gestión del cambio según metodología Kiro SDD:
> 1. Editar `requirements.md` añadiendo US-06 y sus criterios de aceptación
> 2. Actualizar `design.md` con el nuevo modelo y diagrama ER v1.1
> 3. Añadir las tareas de este bloque a `tasks.md`
> 4. Implementar solo las tareas nuevas; las completadas del MVP se preservan

### T-12 · Plataformas de streaming
- [ ] **T-12.1** Crear modelo `Platform` con campos `name` y `slug`
- [ ] **T-12.2** Añadir relación `ManyToManyField` entre `Title` y `Platform`
- [ ] **T-12.3** Crear data migration para cargar las 6 plataformas predefinidas
- [ ] **T-12.4** Añadir campo de plataformas a `TitleForm` (checkboxes)
- [ ] **T-12.5** Actualizar `get_filtered_titles()` para aceptar filtro de plataforma
- [ ] **T-12.6** Añadir selector de plataforma a `_filter_bar.html`
- [ ] **T-12.7** Mostrar las plataformas del título en `_title_card.html`
- [ ] **T-12.8** Verificar que el filtro de plataforma se combina con el de género (AC-06.4)
- [ ] **T-12.9** Añadir tests para las nuevas funcionalidades

*Requisitos cubiertos: US-06 (AC-06.1, AC-06.2, AC-06.3, AC-06.4)*


---

## BLOQUE 9 — Integración TMDB (v1.2 · US-07)

> Activado tras la entrega del MVP. Gestión del cambio según metodología Kiro SDD:
> 1. Editado `requirements.md` añadiendo US-07 y sus criterios de aceptación.
> 2. Actualizado `design.md` con el nuevo modelo, diagrama ER v1.2 y flujo TMDB.
> 3. Añadidas las tareas de este bloque a `tasks.md`.
> 4. Las tareas completadas del MVP se preservan.

### T-13 · Modelo — campo `tmdb_id`, `synopsis` y `poster_url`
- [x] **T-13.1** Añadir campo `tmdb_id` (`PositiveIntegerField`, null/blank, unique, db_index) al modelo `Title`
- [x] **T-13.2** Añadir campo `synopsis` (`TextField`, blank=True) al modelo `Title`
- [x] **T-13.3** Añadir campo `poster_url` (`URLField`, max_length=500, blank=True) al modelo `Title`
- [x] **T-13.4** Crear y aplicar migración (`makemigrations` + `migrate`)

*Requisitos cubiertos: AC-07.4, AC-07.5*

### T-14 · Configuración
- [x] **T-14.1** Añadir variable `TMDB_API_READ_TOKEN` al fichero `.env`
- [x] **T-14.2** Leer `TMDB_API_READ_TOKEN` en `settings.py` mediante `django-environ`
- [x] **T-14.3** Añadir `requests` a `requirements.txt` e instalarlo en el entorno virtual

*Requisitos cubiertos: RNF-05, RNF-06*

### T-15 · Capa de servicios TMDB
- [x] **T-15.1** Implementar `search_tmdb(query: str) -> list[dict]` en `services.py`
  - Llama a `https://api.themoviedb.org/3/search/multi` con el token Bearer
  - Filtra solo resultados de tipo `movie` y `tv`
  - Normaliza cada resultado: `tmdb_id`, `media_type`, `title`, `year`, `genre`, `synopsis`, `poster_url`
  - Gestiona errores de red y HTTP (devuelve lista vacía + log)
- [x] **T-15.2** Implementar `add_from_tmdb(tmdb_id: int, media_type: str, title: str, year: int | None, genre: str, synopsis: str, poster_url: str) -> Title`
  - Comprueba duplicado por `tmdb_id`; lanza `DuplicateTitleError` si ya existe
  - Crea el `Title` con `status="pending"` y los datos recibidos
- [x] **T-15.3** Implementar `map_tmdb_genre(genre_ids: list[int]) -> str` con la tabla de mapeo del diseño
- [x] **T-15.4** Definir excepción `DuplicateTitleError` en `services.py`

*Requisitos cubiertos: AC-07.1, AC-07.4, AC-07.5*

### T-16 · Vistas y URLs
- [x] **T-16.1** Implementar `TmdbSearchView(View)` en `views.py`
  - GET sin parámetros: muestra formulario de búsqueda vacío
  - GET con `?q=<término>`: llama a `search_tmdb()`, pasa resultados al contexto
  - Valida que `q` no esté vacío o solo espacios (AC-07.7)
- [x] **T-16.2** Implementar `TmdbAddView(View)` en `views.py`
  - Solo POST
  - Recibe `tmdb_id`, `media_type`, `title`, `year`, `genre`, `synopsis`, `poster_url` del formulario
  - Llama a `add_from_tmdb()`; captura `DuplicateTitleError` y muestra aviso (AC-07.5)
  - Redirige a `title-list` con mensaje de éxito (AC-07.6)
- [x] **T-16.3** Añadir rutas `tmdb-search` y `tmdb-add` a `watchlist/urls.py`

*Requisitos cubiertos: AC-07.1, AC-07.2, AC-07.3, AC-07.4, AC-07.5, AC-07.6, AC-07.7*

### T-17 · Templates
- [x] **T-17.1** Crear `templates/watchlist/tmdb_search.html` con formulario de búsqueda y grid de resultados
- [x] **T-17.2** Crear partial `templates/watchlist/partials/_tmdb_result_card.html` con póster, título, año, género y botón "Añadir"
- [x] **T-17.3** Añadir enlace "Buscar en TMDB" en `base.html` (navbar) y en el estado vacío de `title_list.html`

*Requisitos cubiertos: AC-07.1, AC-07.2, AC-07.4*


---

## BLOQUE 10 — TMDB como única fuente (v1.3 · US-08)

### T-18 · Navegación y UX
- [x] **T-18.1** Eliminar enlace "Buscar TMDB" de la navbar; convertir el botón "Añadir" en "Añadir título" apuntando a `tmdb-search`
- [x] **T-18.2** Actualizar estado vacío de `title_list.html`: el único botón apunta a `tmdb-search`
- [x] **T-18.3** Actualizar el título/subtítulo de `tmdb_search.html` para reflejar su nuevo rol principal
- [x] **T-18.4** Actualizar docstring de `urls.py` marcando `/add/` como acceso solo interno/admin
