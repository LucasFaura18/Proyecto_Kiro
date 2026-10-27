# Proyecto Kiro — SDD con Kiro IDE

> **Máster de FP en Inteligencia Artificial y Big Data**  
> Práctica: Desarrollo de una aplicación mediante SDD asistido por IA  
> Metodología: **Kiro (Specs)** · Aplicación: **CineTrack**

---

## 📁 Estructura del repositorio

```
Proyecto_Kiro/
├── README.md                        ← Este fichero
├── investigacion_kiro.md            ← Fase 1: Investigación sobre Kiro y SDD
├── flujo_trabajo_kiro.md            ← Diagramas visuales del flujo de trabajo
├── practica_sdd.pdf                 ← Enunciado de la práctica
└── app/
    ├── .kiro/                       ← Configuración de Kiro para la app
    │   ├── steering/                ← Contexto persistente del agente
    │   │   ├── conventions.md       ← Normas de código del proyecto
    │   │   ├── tech-stack.md        ← Stack tecnológico y estructura
    │   │   └── product.md           ← Contexto de negocio y funcionalidades
    │   ├── hooks/                   ← Automatizaciones por eventos del IDE
    │   │   ├── lint-on-save.json    ← Linting al guardar ficheros .py
    │   │   ├── migration-check.json ← Aviso al modificar models.py
    │   │   └── test-on-task-complete.json  ← Tests al completar tarea de spec
    │   └── specs/                   ← Especificaciones SDD
    │       ├── requirements.md      ← Historias de usuario + criterios EARS
    │       ├── design.md            ← Arquitectura, modelos, vistas, diagramas
    │       └── tasks.md             ← Lista de tareas ordenadas por dependencia
    └── src/                         ← Código fuente de la aplicación Django
        ├── requirements.txt
        ├── .env.example
        ├── .gitignore
        ├── pytest.ini
        ├── setup.cfg
        ├── manage.py                ← (generado al inicializar Django)
        ├── config/                  ← Proyecto Django
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        └── watchlist/               ← App principal
            ├── models.py
            ├── views.py
            ├── urls.py
            ├── forms.py
            ├── services.py
            ├── admin.py
            ├── templates/
            └── tests/
```

---

## 🎬 La aplicación — CineTrack

**CineTrack** es una watchlist personal de películas y series construida con Django y Python. Permite gestionar títulos con estado de visionado, puntuación por estrellas y filtrado por género.

### Funcionalidades del MVP (v1.0)

| # | Funcionalidad |
|---|---|
| F1 | Añadir película o serie con título, tipo, género, año y estado |
| F2 | Cambiar el estado de visionado: Pendiente → Viendo → Visto |
| F3 | Puntuar del 1 al 5 los títulos vistos (visualización en estrellas) |
| F4 | Filtrar la lista por género y/o estado |
| F5 | Eliminar un título con confirmación |

### Cambio de requisitos — v1.1

Tras el MVP se añadió la funcionalidad de **plataforma de streaming** (Netflix, HBO Max, Disney+, etc.), gestionado como cambio de requisitos siguiendo la metodología Kiro SDD.

---

## 🚀 Cómo ejecutar la aplicación

### Requisitos previos
- Python 3.11 o superior
- pip

### Pasos

```bash
# 1. Entrar en la carpeta del código fuente
cd app/src

# 2. Crear y activar el entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r app/src/requirements.txt

# 5. Crear la base de datos (SQLite — se genera automáticamente)
python app/src/manage.py migrate

# 6. (Opcional) Crear superusuario para el admin de Django
python app/src/manage.py createsuperuser

# 7. Arrancar el servidor de desarrollo
python app/src/manage.py runserver
```

La aplicación estará disponible en: **http://127.0.0.1:8000**  
Panel de administración: **http://127.0.0.1:8000/admin**

### Ejecutar los tests

```bash
cd app/src
pytest
```

---

## 🔬 Cómo se ha aplicado la metodología Kiro SDD

El desarrollo siguió el flujo de trabajo de Kiro en cuatro etapas:

**1. Preparación (`app/.kiro/`)**  
Antes de escribir una línea de código se configuraron los tres pilares de Kiro: los **steering files** (convenciones, tech stack y contexto de producto), los **hooks** de automatización (lint al guardar, aviso de migraciones, tests al completar tareas) y los ficheros de configuración del proyecto.

**2. Especificación (`app/.kiro/specs/`)**  
A partir de la descripción de la aplicación en lenguaje natural, se generaron los tres documentos de spec antes de implementar nada:
- `requirements.md` — historias de usuario con criterios de aceptación en notación EARS
- `design.md` — arquitectura MTV, modelo de datos, URLs, wireframes y diagramas Mermaid
- `tasks.md` — tareas ordenadas por dependencia, trazadas a sus requisitos

**3. Revisión humana**  
Los documentos fueron revisados y ajustados (por ejemplo, confirmar SQLite nativa de Django, definir el orden de los bloques de tareas) antes de dar la orden de implementación.

**4. Implementación guiada**  
Kiro implementó cada tarea de `tasks.md` en orden, con los hooks verificando calidad en tiempo real. El cambio de requisitos (plataformas, v1.1) se gestionó editando la spec y dejando que Kiro actualizara solo las tareas afectadas.

---

## 📚 Bibliografía y recursos

| Recurso | Enlace |
|---|---|
| Documentación oficial de Kiro | [kiro.dev/docs](https://kiro.dev/docs/) |
| Blog: Introducción a Kiro | [kiro.dev/blog/introducing-kiro](https://kiro.dev/blog/introducing-kiro/) |
| Blog: De chat a specs — deep dive | [kiro.dev/blog/from-chat-to-specs-deep-dive](https://kiro.dev/blog/from-chat-to-specs-deep-dive/) |
| Blog: El futuro del SDD | [kiro.dev/blog/kiro-and-the-future-of-software-development](https://kiro.dev/blog/kiro-and-the-future-of-software-development/) |
| Blog: Steering y MCP | [kiro.dev/blog/teaching-kiro-new-tricks-with-agent-steering-and-mcp](https://kiro.dev/blog/teaching-kiro-new-tricks-with-agent-steering-and-mcp/) |
| Guía completa SDD con Kiro 2026 | [pingax.com/kiro-spec-driven-development](https://pingax.com/kiro-spec-driven-development/) |
| Repositorio oficial de Kiro | [github.com/kirodotdev/Kiro](https://github.com/kirodotdev/Kiro) |
| Documentación de Django 4.2 | [docs.djangoproject.com](https://docs.djangoproject.com/en/4.2/) |
| Bootstrap 5 | [getbootstrap.com](https://getbootstrap.com/) |
| pytest-django | [pytest-django.readthedocs.io](https://pytest-django.readthedocs.io/) |


PARTE A — Datos y Lógica de Negocio (Backend)
Dueña de: config/, models.py, services.py, forms.py, admin.py, migraciones, requirements.txt, settings.py, .env.

Bloque	Tareas	Qué entrega
B0 · Inicialización	T-00.1 → T-00.6	Proyecto Django config + app watchlist, venv, settings (SQLite, español, templates), .env con SECRET_KEY, runserver operativo
B1 · Modelo	T-01.1 → T-01.6	Title con todos los campos y choices, __str__, get_next_status(), registro en admin, migración inicial
B2 · Servicios	T-02.1, T-02.2	get_next_status(current) y get_filtered_titles(genre, status)
B3 · Formularios	T-03.1 → T-03.4	TitleForm(ModelForm) con clean() (limpiar rating si no es watched, validar year 1888–actual+2) y widgets Bootstrap 5
v1.1	T-12.1 → T-12.5	Modelo Platform, ManyToManyField, data migration de las 6 plataformas, campo en TitleForm, extensión de get_filtered_titles() con filtro de plataforma
Tests propios (opcional pero recomendado): T-11.1 (get_next_status), T-11.2 (TitleForm.clean), T-11.3 (get_filtered_titles).

PARTE B — Vistas, Plantillas y Calidad (Frontend + Controlador + QA)
Dueña de: views.py, urls.py, todo templates/ (base.html, partials y plantillas de página) y tests/ de vistas.

Bloque	Tareas	Qué entrega
B4 · Templates base	T-04.1 → T-04.4	base.html (navbar + Bootstrap/Font Awesome CDN), partials _star_rating.html, _filter_bar.html, _title_card.html
B5 · Vistas y URLs	T-05 → T-09	TitleListView (con filtros GET), TitleCreateView, TitleUpdateView, TitleStatusUpdateView (POST), TitleDeleteView; urls.py con name=; plantillas title_list.html, title_form.html, title_confirm_delete.html; botones de estado/estrellas en _title_card.html
B6 · No funcionales	T-10.1 → T-10.3	Responsive a 375px, aria-label en botones, role="alert" en errores de formulario
B7 · Tests	T-11.4, T-11.5	Tests de TitleCreateView (POST válido/inválido) y TitleStatusUpdateView (avance de estado)
v1.1	T-12.6 → T-12.9	Selector de plataforma en _filter_bar.html, plataformas en _title_card.html, verificación de combinación de filtros, tests de plataforma
Contrato de interfaz (lo que A expone y B consume)
Como ambos trabajamos contra design.md, B no necesita que A termine para empezar las plantillas base, pero sí para conectar las vistas. A debe respetar exactamente estos nombres:

Modelo Title: campos name, title_type, genre, year, status, rating, notes, created_at, updated_at y los choices TYPE_CHOICES, GENRE_CHOICES, STATUS_CHOICES del diseño.
Servicios: get_next_status(current: str) -> str, get_filtered_titles(genre, status) -> QuerySet.
Formulario: TitleForm con los 7 campos del diseño y widgets con clases form-control/form-select (para que las plantillas de B rendericen sin tocar el form).
Fases de ejecución (paralelizable)

Fase 1  A: T-00 (esqueleto Django)  ── bloqueante para todos
Fase 2  A: T-01, T-02, T-03  ║  B: T-04 (templates base desde design.md)
Fase 3  B: T-05 → T-09 (necesita modelo+servicios+form de A listos)
Fase 4  A: tests de su capa (T-11.1–11.3)  ║  B: T-10 + tests de vistas (T-11.4–11.5)
Fase 5  v1.1: A: T-12.1–12.5  →  B: T-12.6–12.9
B puede arrancar la Fase 2 a la vez que A construye el modelo, porque base.html y los partials se hacen contra el diseño, no contra el código. El punto de sincronización real es el inicio de la Fase 3, cuando A ya tiene Title, services.py y TitleForm.

Notas de coordinación
Sin conflictos de ficheros: A nunca toca templates/, B nunca toca models.py/services.py/forms.py. El db.sqlite3 y las migraciones los genera A.
Tests: por la convención "un fichero de test por app", propongo 
test_models.py
 y test_services.py (A) + 
test_views.py
 (B). Cada uno testea su capa.
Hooks: ya existen lint-on-save y test-on-task-complete; ambos os avisan al guardar/guardar tarea, así que da igual en qué fichero trabajéis.
v1.1: es un cambio de requisitos formal. Hay que editar antes requirements.md (US-06 ya está) y design.md (diagrama ER v1.1 ya está), según el bloque 8 de tasks.md. A hace la parte de datos y B la de presentación, en ese orden.
¿Quieres que marque directamente esta asignación en tasks.md (por ejemplo etiquetando cada tarea con [A] / [B]) para que quede trazado en el repo, o prefieres dejarlo solo como plan?


https://gamma.app/docs/Desarrollo-con-IA-Spec-Driven-Development-con-Kiro-2qtpiud0scni56k