# Investigación: Kiro y el Spec-Driven Development (SDD)

> **Máster de FP en Inteligencia Artificial y Big Data**  
> Práctica: Desarrollo de una aplicación mediante SDD asistido por IA  
> Metodología investigada: **Kiro (Specs)**

---

## 1. Descripción General

**Kiro** es un entorno de desarrollo integrado (IDE) con IA, desarrollado por **Amazon Web Services (AWS)**, lanzado en julio de 2025. Está construido sobre **Visual Studio Code** (Code OSS), por lo que mantiene compatibilidad con la configuración, extensiones y flujos de trabajo existentes de VS Code.

Su propuesta diferencial frente a otras herramientas de IA (como GitHub Copilot o Cursor) es el **Spec-Driven Development (SDD)**: un modelo de trabajo en el que la IA no genera código de inmediato ante un prompt, sino que primero elabora una especificación estructurada y revisable que el desarrollador debe aprobar antes de que comience la implementación.

> *"Spec-driven development positions AI as your strategic thinking partner, helping you make better decisions before they become expensive to change."*  
> — [Kiro Blog](https://kiro.dev/blog/from-chat-to-specs-deep-dive/)

### ¿Por qué SDD?

El problema con los asistentes de IA tradicionales es predecible: cuando el desarrollador da un prompt de alto nivel, la IA salta directamente a generar código antes de entender bien los requisitos. Esto provoca:

- Ciclos de "en realidad quería decir..." que consumen el contexto.
- Código técnicamente válido pero que no encaja con las convenciones del equipo.
- Decisiones de diseño implícitas que nadie documentó.
- Documentación que queda desfasada desde el primer día.

Kiro resuelve esto haciendo que **la especificación sea el artefacto central del desarrollo**.

---

## 2. Fases del Proceso de Desarrollo con Kiro

El flujo de trabajo con Kiro Specs sigue **4 pasos claros**:

### Paso 1 — Descripción de la intención (en lenguaje natural)

El desarrollador describe en lenguaje natural qué quiere construir, sin necesidad de sintaxis formal. Kiro analiza el prompt en el contexto del proyecto existente.

```
"Añadir un sistema de reseñas para los productos de la tienda,
con valoración por estrellas y filtrado por puntuación."
```

### Paso 2 — Kiro genera la especificación

Kiro **no genera código**. En su lugar, produce tres documentos Markdown estructurados que quedan guardados en el repositorio:

| Fichero | Contenido |
|---|---|
| `requirements.md` | Historias de usuario con criterios de aceptación en notación **EARS** (Easy Approach to Requirements Syntax), incluyendo casos límite |
| `design.md` | Decisiones de arquitectura, diagramas de flujo (Mermaid), interfaces de datos, esquemas de base de datos y endpoints de API |
| `tasks.md` | Lista de tareas y subtareas ordenadas por dependencias, cada una enlazada a su requisito |

> Kiro analiza el código existente para generar estos documentos de forma coherente con la arquitectura actual del proyecto.

### Paso 3 — Revisión y edición humana

Antes de que se escriba una sola línea de código, el desarrollador revisa los documentos y puede modificarlos. Corregir la especificación toma 5–15 minutos; corregir código mal generado puede costar horas.

Ejemplo de ajuste típico en esta fase:
```markdown
# Edición en requirements.md
- Cambiar: output como tabla en base de datos
+ Cambiar: output como fichero Parquet en S3
- Usar polars en lugar de pandas (según nuestras convenciones)
```

### Paso 4 — Implementación guiada por la especificación

Al hacer clic en "Implement", Kiro genera el código siguiendo la especificación aprobada, los documentos de *steering* del proyecto y las buenas prácticas del stack tecnológico. Cada cambio en el código queda trazable hasta un requisito concreto.

---

## 3. Herramientas y Documentos Empleados

Kiro organiza su funcionalidad en torno a **cuatro pilares** que se complementan con el flujo de Specs:

### 3.1 Specs (Especificaciones)

Artefactos Markdown almacenados en `.kiro/specs/` que formalizan los requisitos, el diseño y las tareas. Son **documentación viva**: si el código cambia, Kiro puede actualizar las specs, y si las specs cambian a mitad de la implementación, Kiro ajusta su plan.

### 3.2 Steering (Reglas de contexto persistente)

Ficheros Markdown en `.kiro/steering/` que proporcionan contexto permanente al agente: convenciones de código, estructura del proyecto, librerías preferidas, estándares del equipo, etc.

Modos de inclusión:
- **Siempre activo** (por defecto): se inyecta en cada interacción.
- **Por patrón de fichero** (`inclusion: fileMatch`): solo cuando se trabaja con ciertos ficheros.
- **Manual** (`inclusion: manual`): el desarrollador lo activa explícitamente con `#`.
- **Automático** (`inclusion: auto`): Kiro lo activa cuando el contexto es relevante.

Ejemplo de steering:
```markdown
# Convenciones del proyecto
- Usar polars, no pandas.
- Todas las conexiones a BD a través de SQLAlchemy pool.
- Nunca hardcodear credenciales — usar Secrets Manager.
- Todas las funciones necesitan type hints y docstrings Google.
```

> Una vez configurados, **todos los ficheros generados por IA siguen estas convenciones automáticamente**, sin necesidad de repetirlas en cada prompt.

### 3.3 Hooks (Automatizaciones por eventos)

Ficheros JSON en `.kiro/hooks/` que ejecutan comandos o agentes automáticamente ante eventos del IDE. Funcionan como un colaborador senior que verifica el trabajo en segundo plano.

Eventos disponibles:
- `PostFileSave` — al guardar un fichero
- `PostFileCreate` — al crear un fichero nuevo
- `PostFileDelete` — al borrar un fichero
- `PreToolUse` / `PostToolUse` — antes/después de que el agente use una herramienta
- `PreTaskExec` / `PostTaskExec` — antes/después de ejecutar una tarea de la spec
- `SessionStart` — al iniciar una sesión
- `UserPromptSubmit` — al enviar un mensaje al agente

Ejemplo de hook para validar componentes React al guardar:
```json
{
  "version": "v1",
  "hooks": [{
    "name": "Validar principio de responsabilidad única",
    "trigger": "PostFileSave",
    "matcher": "\\.(tsx|jsx)$",
    "action": {
      "type": "agent",
      "prompt": "Verifica que el componente guardado sigue el Single Responsibility Principle."
    }
  }]
}
```

### 3.4 Agentes personalizados (Custom Agents)

Ficheros de configuración en `.kiro/agents/` que definen agentes especializados con:
- Herramientas específicas habilitadas/deshabilitadas.
- Prompt del sistema propio.
- Permisos acotados a partes del proyecto.
- Conexión a servidores MCP específicos.

### 3.5 MCP (Model Context Protocol)

Protocolo abierto para conectar herramientas externas al agente: bases de datos, APIs, servicios cloud, documentación propietaria, etc. Configurado en `.kiro/settings/mcp.json`.

### 3.6 Tipos de sesión y modos de autonomía

| Dimensión | Opción A | Opción B |
|---|---|---|
| **Tipo de sesión** | **Vibe** — conversacional, exploración libre | **Spec** — flujo estructurado de requisitos → diseño → tareas |
| **Modo de autonomía** | **Autopilot** — Kiro trabaja de forma autónoma de principio a fin | **Supervised** — Kiro presenta cada cambio como hunk individual para aprobar/rechazar |

---

## 4. Ejemplos Concretos de Utilización

### Ejemplo 1: Nueva funcionalidad desde cero

**Contexto:** Aplicación de e-commerce, se quiere añadir un sistema de reseñas.

1. El desarrollador escribe en modo Spec: *"Add a review system for products"*
2. Kiro genera `requirements.md` con historias de usuario (ver reseñas, crear reseña, filtrar por valoración, responder a reseña) y criterios de aceptación EARS para cada una.
3. `design.md` incluye: interfaces TypeScript `Review`, esquema de tabla `reviews` en PostgreSQL, endpoint `POST /api/products/:id/reviews` y diagrama Mermaid del flujo de datos.
4. `tasks.md` desglosa: crear migración de BD → implementar repositorio → crear endpoint → crear componente React → escribir tests unitarios → tests de integración → accesibilidad y responsive.
5. El desarrollador revisa, aprueba y lanza la implementación tarea a tarea.

### Ejemplo 2: Gestión de cambio de requisitos

Si a mitad de la implementación el cliente pide que el sistema de reseñas incluya también moderación por parte del administrador:
1. Se edita `requirements.md` para añadir la historia de usuario de moderación.
2. Kiro detecta el cambio y actualiza `design.md` y `tasks.md` en consecuencia.
3. Las tareas ya completadas se preservan; solo se añaden/modifican las afectadas.

### Ejemplo 3: Hook de seguridad en commits

```json
{
  "version": "v1",
  "hooks": [{
    "name": "Escaneo de credenciales",
    "trigger": "PreToolUse",
    "matcher": "execute_pwsh",
    "action": {
      "type": "command",
      "command": "git secrets --scan"
    }
  }]
}
```
Cada vez que el agente intenta ejecutar un comando de shell, se escanea automáticamente en busca de credenciales hardcodeadas.

---

## 5. Principales Ventajas e Inconvenientes

### ✅ Ventajas

| Ventaja | Descripción |
|---|---|
| **Requisitos explícitos** | Las ambigüedades se resuelven antes de escribir código, no durante. |
| **Trazabilidad** | Cada línea de código puede rastrearse hasta un requisito de la spec. |
| **Documentación automática** | Los ficheros de spec *son* la documentación del sistema, y se mantienen vivos. |
| **Gestión del contexto** | Al externalizar la planificación a ficheros, el contexto del LLM se reserva para la tarea de código actual. |
| **Consistencia de equipo** | Los ficheros de steering y hooks se versionan en Git y aplican las mismas reglas a todos los miembros. |
| **Control humano** | El modo Supervised permite aprobar cada cambio individualmente; la revisión de specs es un punto de control natural. |
| **Adaptable a código existente** | Kiro puede analizar una base de código existente y generar specs retroactivamente. |
| **Compatible con VS Code** | Configuración, extensiones y atajos de teclado existentes siguen funcionando. |

### ❌ Inconvenientes / Limitaciones

| Inconveniente | Descripción |
|---|---|
| **Overhead para tareas pequeñas** | Para bugfixes de una línea o refactorizaciones triviales, crear una spec es excesivo. |
| **Curva de aprendizaje inicial** | Requiere adoptar un flujo de trabajo diferente al de otros asistentes de IA. |
| **Calidad dependiente del prompt inicial** | Si la descripción inicial es vaga, la spec generada también lo será. |
| **Herramienta nueva (2025)** | Ecosistema y comunidad más pequeños que herramientas maduras como Copilot o Cursor. |
| **Dependencia de AWS** | Al estar desarrollado por AWS, su roadmap y disponibilidad dependen de decisiones de Amazon. |

---

## 6. Comparativa con otras herramientas SDD

| Dimensión | **Kiro SDD** | Cursor / Copilot |
|---|---|---|
| Dónde se define la intención | En la spec — artefacto revisable antes de la implementación | En el prompt — se pierde al cerrar la conversación |
| Revisabilidad | ✅ Spec editable y versionada en Git | ❌ El prompt es efímero |
| Alineación de equipo | ✅ Spec compartible y aprobable | ❌ Cada desarrollador interpreta a su manera |
| Documentación | ✅ La spec es la documentación | ❌ Hay que escribirla aparte |
| Cuando la intención es incorrecta | Editar spec y re-implementar (~10 min) | Re-prompting y depuración (~horas) |
| Trazabilidad | ✅ Cada cambio vinculado a un requisito | ❌ Sin trazabilidad formal |

---

## 7. Conclusión

Kiro representa una evolución en el desarrollo asistido por IA: pasa de usar la IA como un **generador de código avanzado** a usarla como un **partner de ingeniería** que planifica, documenta e implementa de forma estructurada.

El SDD de Kiro es especialmente valioso cuando:
- Se construyen funcionalidades nuevas desde cero.
- El proyecto involucra a varios desarrolladores.
- Se necesita trazabilidad o auditoría de decisiones técnicas.
- Se gestionan cambios de requisitos (el caso de uso de esta práctica).

Y es menos necesario cuando:
- Se hacen correcciones puntuales o exploración rápida.
- El alcance de la tarea es trivial y perfectamente claro.

> *"El objetivo no es demostrar cuánto código puede generar una IA, sino aprender a dirigir y supervisar el desarrollo de software asistido por IA."*  
> — Enunciado de la práctica

Kiro, precisamente, está diseñado con esa filosofía en su núcleo.

---

## 8. Recursos y Bibliografía

| Recurso | Enlace |
|---|---|
| Documentación oficial de Kiro | [kiro.dev/docs](https://kiro.dev/docs/) |
| Blog: Introducción a Kiro | [kiro.dev/blog/introducing-kiro](https://kiro.dev/blog/introducing-kiro/) |
| Blog: De chat a specs — deep dive | [kiro.dev/blog/from-chat-to-specs-deep-dive](https://kiro.dev/blog/from-chat-to-specs-deep-dive/) |
| Blog: El futuro del desarrollo con SDD | [kiro.dev/blog/kiro-and-the-future-of-software-development](https://kiro.dev/blog/kiro-and-the-future-of-software-development/) |
| Blog: Steering y MCP | [kiro.dev/blog/teaching-kiro-new-tricks-with-agent-steering-and-mcp](https://kiro.dev/blog/teaching-kiro-new-tricks-with-agent-steering-and-mcp/) |
| Guía completa SDD con Kiro (2026) | [pingax.com/kiro-spec-driven-development](https://pingax.com/kiro-spec-driven-development/) |
| Repositorio oficial de Kiro | [github.com/kirodotdev/Kiro](https://github.com/kirodotdev/Kiro) |
| Verdent AI: Kiro SDD Requirements to Code | [verdent.ai/guides/agents/kiro-spec-driven-development](https://www.verdent.ai/guides/agents/kiro-spec-driven-development) |
| Dev.to: Stop Chatting, Start Specifying | [dev.to/kirodotdev/stop-chatting-start-specifying](https://dev.to/kirodotdev/stop-chatting-start-specifying-spec-driven-design-with-kiro-ide-3b3o) |
| Dev.to: Spec-driven dev con Kiro en re:Invent 2025 | [dev.to/aws/dev-track-spotlight-spec-driven-development-with-kiro](https://dev.to/aws/dev-track-spotlight-spec-driven-development-with-kiro-dev314-45e8) |
