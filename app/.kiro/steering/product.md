# Contexto de Producto — CineTrack

## ¿Qué es CineTrack?
CineTrack es una aplicación web sencilla para gestionar una lista personal de películas y series. Permite al usuario llevar un registro de lo que ha visto, lo que está viendo y lo que tiene pendiente, con puntuación propia y filtrado por género.

## Usuario objetivo
Una persona que consume contenido audiovisual habitualmente y quiere tener un registro organizado sin depender de apps externas como Letterboxd o IMDb.

## Funcionalidades del MVP (v1.0)

| # | Funcionalidad | Descripción breve |
|---|---|---|
| F1 | **Añadir título** | Registrar una peli/serie con título, tipo, género, año y estado |
| F2 | **Marcar como visto** | Cambiar el estado de un título (Pendiente → Viendo → Visto) |
| F3 | **Puntuar** | Asignar una puntuación del 1 al 5 a los títulos vistos |
| F4 | **Filtrar por género** | Ver solo los títulos de un género concreto |
| F5 | **Eliminar título** | Borrar un título de la lista con confirmación |

## Cambio de requisitos planificado (v1.1)
Tras el MVP, se introducirá la siguiente funcionalidad:

**F6 — Plataforma de streaming disponible**
- Añadir a cada título en qué plataforma(s) está disponible (Netflix, HBO Max, Disney+, Prime Video, Movistar+, Otros)
- Filtrar la lista también por plataforma
- Esta funcionalidad requiere modificar el modelo de datos y añadir un nuevo filtro en la vista principal

## Lo que CineTrack NO hace (fuera de alcance)
- No gestiona usuarios ni autenticación
- No conecta con APIs externas (TMDB, IMDB...)
- No tiene sistema de recomendaciones
- No permite compartir listas

## Métricas de éxito del MVP
- El usuario puede añadir un título en menos de 30 segundos
- La lista es filtrable sin recargar la página (o con recarga mínima)
- La interfaz es usable en móvil
