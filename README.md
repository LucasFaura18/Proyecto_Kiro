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
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Editar .env y establecer una SECRET_KEY

# 5. Crear la base de datos (SQLite — se genera automáticamente)
python manage.py migrate

# 6. (Opcional) Crear superusuario para el admin de Django
python manage.py createsuperuser

# 7. Arrancar el servidor de desarrollo
python manage.py runserver
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
