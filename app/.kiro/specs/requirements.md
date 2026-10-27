# Requirements — CineTrack MVP (v1.0)

> Generado siguiendo la metodología Kiro SDD  
> Notación de criterios de aceptación: **EARS** (Easy Approach to Requirements Syntax)

---

## Historias de usuario

---

### US-01 · Añadir un título a la watchlist

**Como** usuario,  
**quiero** poder añadir una película o serie a mi lista,  
**para** tener un registro de lo que quiero ver o he visto.

#### Criterios de aceptación

| ID | Criterio (EARS) |
|---|---|
| AC-01.1 | **When** el usuario rellena el formulario con título, tipo (película/serie), género y estado y pulsa "Guardar", **then** el título aparece en la lista principal. |
| AC-01.2 | **When** el usuario envía el formulario sin título, **then** el sistema muestra un mensaje de error "El título es obligatorio" y no guarda el registro. |
| AC-01.3 | **When** el usuario añade un título, **then** el campo de puntuación es opcional y puede dejarse vacío. |
| AC-01.4 | **Where** el estado inicial no es "Visto", **then** el campo de puntuación queda deshabilitado. |
| AC-01.5 | **When** el título se añade correctamente, **then** el sistema redirige a la lista principal con un mensaje de confirmación. |

---

### US-02 · Cambiar el estado de visionado

**Como** usuario,  
**quiero** poder cambiar el estado de un título (Pendiente / Viendo / Visto),  
**para** mantener actualizado mi progreso de visionado.

#### Criterios de aceptación

| ID | Criterio (EARS) |
|---|---|
| AC-02.1 | **When** el usuario pulsa el botón de cambio de estado en un título, **then** el estado cambia al siguiente en la secuencia: Pendiente → Viendo → Visto. |
| AC-02.2 | **When** el estado cambia a "Visto", **then** el campo de puntuación se activa para ese título. |
| AC-02.3 | **When** el estado cambia de "Visto" a cualquier otro, **then** la puntuación existente se conserva pero se deshabilita visualmente. |
| AC-02.4 | **While** el usuario está en la lista principal, **then** puede cambiar el estado sin entrar al detalle del título. |

---

### US-03 · Puntuar un título

**Como** usuario,  
**quiero** poder puntuar del 1 al 5 los títulos que he visto,  
**para** recordar cuánto me gustó cada uno.

#### Criterios de aceptación

| ID | Criterio (EARS) |
|---|---|
| AC-03.1 | **When** el título tiene estado "Visto", **then** el usuario puede seleccionar una puntuación del 1 al 5 representada con estrellas. |
| AC-03.2 | **When** el usuario guarda una puntuación, **then** las estrellas correspondientes se muestran en la tarjeta del título. |
| AC-03.3 | **When** el título no tiene estado "Visto", **then** el control de puntuación aparece deshabilitado. |
| AC-03.4 | **When** el usuario cambia una puntuación existente y guarda, **then** la nueva puntuación reemplaza a la anterior. |

---

### US-04 · Filtrar la lista por género

**Como** usuario,  
**quiero** poder filtrar mi watchlist por género,  
**para** encontrar rápidamente títulos de un tipo concreto.

#### Criterios de aceptación

| ID | Criterio (EARS) |
|---|---|
| AC-04.1 | **When** el usuario selecciona un género en el filtro, **then** la lista muestra solo los títulos de ese género. |
| AC-04.2 | **When** el usuario selecciona "Todos" en el filtro de género, **then** se muestran todos los títulos sin filtrar. |
| AC-04.3 | **When** no hay títulos que coincidan con el filtro seleccionado, **then** se muestra el mensaje "No hay títulos en esta categoría". |
| AC-04.4 | **While** se aplica un filtro de género, **then** el filtro de estado (si existe) también se aplica simultáneamente. |

---

### US-05 · Eliminar un título

**Como** usuario,  
**quiero** poder eliminar un título de mi lista,  
**para** mantener la lista limpia y actualizada.

#### Criterios de aceptación

| ID | Criterio (EARS) |
|---|---|
| AC-05.1 | **When** el usuario pulsa "Eliminar" en un título, **then** el sistema muestra una pantalla de confirmación antes de borrar. |
| AC-05.2 | **When** el usuario confirma la eliminación, **then** el título desaparece de la lista y se muestra un mensaje de confirmación. |
| AC-05.3 | **When** el usuario cancela la eliminación, **then** el título se conserva y el usuario vuelve a la lista. |

---

## Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | La interfaz debe ser usable en dispositivos móviles (diseño responsive). |
| RNF-02 | El tiempo de carga de la lista principal no debe superar 2 segundos con hasta 200 títulos. |
| RNF-03 | La aplicación debe funcionar sin conexión a internet (solo usa BD local). |
| RNF-04 | Los errores de formulario deben ser accesibles (etiquetas ARIA). |

---

## Cambio de requisitos planificado — v1.1

### US-06 · Añadir plataforma de streaming

**Como** usuario,  
**quiero** indicar en qué plataforma(s) está disponible un título,  
**para** saber dónde buscarlo cuando quiera verlo.

#### Criterios de aceptación

| ID | Criterio (EARS) |
|---|---|
| AC-06.1 | **When** el usuario añade o edita un título, **then** puede seleccionar una o varias plataformas de una lista predefinida (Netflix, HBO Max, Disney+, Prime Video, Movistar+, Otros). |
| AC-06.2 | **When** el usuario filtra por plataforma, **then** la lista muestra solo los títulos disponibles en esa plataforma. |
| AC-06.3 | **When** un título no tiene plataforma asignada, **then** aparece como "Sin plataforma asignada". |
| AC-06.4 | **When** se añade el filtro de plataforma, **then** puede combinarse con el filtro de género existente. |

---

## Cambio de requisitos — v1.2 (Integración TMDB · US-07)

> Añadido siguiendo la metodología Kiro SDD. Las historias US-01–US-06 se preservan íntegras.

---

### US-07 · Buscar títulos mediante la API de TMDB y añadirlos a la watchlist

**Como** usuario,  
**quiero** poder buscar películas y series por nombre usando la base de datos de TMDB,  
**para** añadirlas a mi watchlist sin tener que introducir manualmente todos los datos.

#### Criterios de aceptación

| ID | Criterio (EARS) |
|---|---|
| AC-07.1 | **When** el usuario introduce un término de búsqueda y pulsa "Buscar", **then** el sistema muestra una lista de resultados con póster, título, año, géneros y sinopsis obtenidos de TMDB. |
| AC-07.2 | **When** la búsqueda no devuelve resultados, **then** el sistema muestra el mensaje "No se han encontrado resultados para «<término>»." |
| AC-07.3 | **When** la API de TMDB no está disponible o devuelve error, **then** el sistema muestra un mensaje de error amigable y no interrumpe las demás funcionalidades. |
| AC-07.4 | **When** el usuario pulsa "Añadir a mi lista" en un resultado, **then** el título se crea en la watchlist con los datos prefijados de TMDB (nombre, tipo, año, géneros → genre mapeado, sinopsis → notes) y estado "Pendiente". |
| AC-07.5 | **When** el usuario intenta añadir un título que ya existe en su watchlist (mismo `tmdb_id`), **then** el sistema muestra un aviso "Este título ya está en tu lista" y no crea un duplicado. |
| AC-07.6 | **When** el usuario añade un resultado de TMDB, **then** el sistema redirige a la lista principal con un mensaje de confirmación. |
| AC-07.7 | **When** la búsqueda contiene solo espacios o está vacía, **then** el sistema no llama a la API y muestra un aviso de validación. |

---

## Requisitos no funcionales adicionales (v1.2)

| ID | Requisito |
|---|---|
| RNF-05 | El token de la API de TMDB se almacena exclusivamente en `.env` y nunca se incluye en el código fuente ni en Git. |
| RNF-06 | Las llamadas a la API de TMDB se realizan desde el backend Django; el navegador nunca recibe ni expone el token. |

---

## Cambio de requisitos — v1.3 (TMDB como única fuente · US-08)

### US-08 · TMDB como único punto de entrada para añadir títulos

**Como** usuario,  
**quiero** que la única forma de añadir un título sea buscándolo en TMDB,  
**para** garantizar que todos los títulos de mi lista tienen datos reales y consistentes (póster, sinopsis, año correcto).

#### Criterios de aceptación

| ID | Criterio (EARS) |
|---|---|
| AC-08.1 | **When** el usuario pulsa "Añadir título" en cualquier parte de la app, **then** el sistema le lleva directamente a la búsqueda TMDB, nunca al formulario manual. |
| AC-08.2 | **When** el usuario accede a la URL `/add/` directamente, **then** el formulario sigue siendo funcional (uso interno/admin), pero no aparece en la navegación pública. |
| AC-08.3 | **When** la lista está vacía, **then** el botón de acción vacía lleva a la búsqueda TMDB. |
