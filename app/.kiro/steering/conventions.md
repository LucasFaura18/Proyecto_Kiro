# Convenciones del Proyecto — CineTrack

## Lenguaje y estilo
- Todo el código en Python 3.11+
- Seguir PEP 8 estrictamente
- Type hints obligatorios en todas las funciones y métodos
- Docstrings en formato Google en español
- Nombres de variables y funciones en inglés (snake_case)
- Nombres de clases en inglés (PascalCase)
- Comentarios en español

## Django
- Usar Django 4.2 LTS
- Un modelo por fichero cuando el modelo es complejo
- Las vistas deben ser class-based views (CBV) siempre que sea posible
- Usar Django ORM, nunca SQL crudo salvo casos justificados
- Toda lógica de negocio va en los modelos o en un fichero `services.py`, nunca en las vistas
- Las URLs deben tener nombres (`name=`) siempre
- Usar `reverse_lazy` en CBVs, `reverse` en funciones

## Base de datos
- Base de datos: SQLite para desarrollo, configurable vía variable de entorno para producción
- Nunca hacer migraciones sin revisar el diff generado
- Los campos opcionales usan `blank=True, null=True` solo cuando es semánticamente correcto

## Formularios y validación
- Usar Django Forms o ModelForms, nunca validar en la vista
- Los errores de formulario deben mostrarse en el template de forma accesible

## Templates
- Usar herencia de templates: `base.html` como plantilla raíz
- Bootstrap 5 como framework CSS (CDN)
- No incluir JavaScript inline en los templates; usar ficheros `.js` separados
- Todas las páginas deben ser responsive

## Seguridad
- Nunca hardcodear la `SECRET_KEY` — usar variables de entorno
- Usar `django-environ` o `python-decouple` para la configuración
- Fichero `.env` en `.gitignore` siempre
- CSRF protection activa en todos los formularios

## Testing
- Tests con `pytest-django`
- Un fichero de test por app Django
- Nombrar tests como `test_<lo_que_prueba>.py`
