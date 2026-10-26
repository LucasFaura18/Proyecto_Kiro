# Flujo de Trabajo Óptimo con Kiro

> Guía visual del proceso completo de **Spec-Driven Development** con Kiro IDE

---

## 🗺️ Vista General del Proceso

```mermaid
flowchart TD
    A([🧑‍💻 DESARROLLADOR\nTiene una idea / requisito]) --> B

    subgraph PREP ["⚙️ 0 · PREPARACIÓN DEL PROYECTO"]
        B[Crear ficheros de Steering\n.kiro/steering/*.md] --> C[Definir Hooks de automatización\n.kiro/hooks/*.json]
        C --> D[Conectar servidores MCP\n.kiro/settings/mcp.json]
    end

    D --> E

    subgraph SPEC ["📋 1 · FASE SPEC — Planificación"]
        E[Elegir modo:\n🎯 Spec Session] --> F
        F[✍️ Describir intención\nen lenguaje natural] --> G
        G[🤖 Kiro analiza\nel codebase existente] --> H
        H[📄 Kiro genera\nrequirements.md] --> I
        I[🏗️ Kiro genera\ndesign.md] --> J
        J[✅ Kiro genera\ntasks.md]
    end

    J --> K

    subgraph REVIEW ["🔍 2 · REVISIÓN HUMANA — Checkpoint"]
        K{¿La spec\nes correcta?}
        K -- ❌ No --> L[Editar requirements.md\ndesign.md o tasks.md]
        L --> K
        K -- ✅ Sí --> M[Aprobar especificación]
    end

    M --> N

    subgraph IMPL ["🚀 3 · IMPLEMENTACIÓN — Ejecución"]
        N[Elegir modo de autonomía] --> O
        O{Modo de\nautonomía}
        O -- Autopilot --> P[Kiro ejecuta todas\nlas tareas en secuencia]
        O -- Supervised --> Q[Kiro presenta cada cambio\ncomo hunk individual]
        Q --> R{¿Aceptar\ncambio?}
        R -- ✅ Accept --> S[Cambio aplicado]
        R -- ❌ Reject --> T[Kiro regenera\ncon ajustes]
        T --> R
        S --> U{¿Más tareas?}
        P --> U
        U -- Sí --> P
        U -- No --> V[✅ Implementación\ncompletada]
    end

    V --> W

    subgraph CHANGE ["🔄 4 · GESTIÓN DEL CAMBIO"]
        W{¿Cambian\nlos requisitos?}
        W -- Sí --> X[Editar spec\nmanualmente]
        X --> Y[Kiro detecta cambio\ny actualiza tasks.md]
        Y --> Z[Solo se regeneran\nlas tareas afectadas]
        Z --> N
        W -- No --> END
    end

    END([🎉 MVP listo\npara producción])

    style PREP fill:#1e3a5f,color:#fff,stroke:#4a9eff
    style SPEC fill:#1a3a2a,color:#fff,stroke:#4ade80
    style REVIEW fill:#3a2a1a,color:#fff,stroke:#fb923c
    style IMPL fill:#2a1a3a,color:#fff,stroke:#c084fc
    style CHANGE fill:#3a1a2a,color:#fff,stroke:#f472b6
```

---

## 📁 Estructura de Ficheros del Proyecto

```mermaid
graph LR
    ROOT["📁 proyecto/"] --> KIRO["📁 .kiro/"]
    ROOT --> SRC["📁 src/"]
    ROOT --> README["📄 README.md"]

    KIRO --> SPECS["📁 specs/"]
    KIRO --> STEERING["📁 steering/"]
    KIRO --> HOOKS["📁 hooks/"]
    KIRO --> AGENTS["📁 agents/"]
    KIRO --> SETTINGS["📁 settings/"]

    SPECS --> REQ["📄 requirements.md\n✍️ Historias de usuario\n+ criterios EARS"]
    SPECS --> DES["📄 design.md\n🏗️ Arquitectura, interfaces,\ndiagramas Mermaid"]
    SPECS --> TASKS["📄 tasks.md\n✅ Tareas ordenadas\npor dependencias"]

    STEERING --> ST1["📄 conventions.md\nNormas de código"]
    STEERING --> ST2["📄 tech-stack.md\nLibrerías y patrones"]
    STEERING --> ST3["📄 product.md\nContexto de negocio"]

    HOOKS --> H1["📄 lint-on-save.json\nLinting automático"]
    HOOKS --> H2["📄 test-update.json\nActualizar tests"]
    HOOKS --> H3["📄 security-scan.json\nEscaneo credenciales"]

    SETTINGS --> MCP["📄 mcp.json\nServidores externos"]

    style REQ fill:#1a3a2a,color:#fff,stroke:#4ade80
    style DES fill:#1a3a2a,color:#fff,stroke:#4ade80
    style TASKS fill:#1a3a2a,color:#fff,stroke:#4ade80
    style ST1 fill:#1e3a5f,color:#fff,stroke:#4a9eff
    style ST2 fill:#1e3a5f,color:#fff,stroke:#4a9eff
    style ST3 fill:#1e3a5f,color:#fff,stroke:#4a9eff
    style H1 fill:#3a2a1a,color:#fff,stroke:#fb923c
    style H2 fill:#3a2a1a,color:#fff,stroke:#fb923c
    style H3 fill:#3a2a1a,color:#fff,stroke:#fb923c
```

---

## ⚙️ Los Tres Pasos de Preparación — ¿Qué son y para qué sirven?

> Estos tres pasos se configuran **una sola vez por proyecto** y definen cómo Kiro se comportará en todas las sesiones futuras. Son la base sobre la que se apoya todo el flujo SDD.

---

### 📌 Paso 1 — Steering files · `.kiro/steering/*.md`

**Son instrucciones permanentes que Kiro lee antes de cada acción.**

Piénsalo como el *briefing que le darías a un desarrollador nuevo el primer día*: qué librerías usa el proyecto, cómo se nombran las variables, qué patrones seguimos, qué está prohibido. Sin steering, Kiro toma decisiones basándose en su conocimiento general. Con steering, toma decisiones según **tus** reglas.

A partir de estos ficheros, **todo el código que genere Kiro** seguirá esas convenciones automáticamente, sin necesidad de repetirlas en cada prompt.

**Ejemplo — `conventions.md`:**
```markdown
# Convenciones del proyecto
- Usar TypeScript estricto, nunca `any`
- Componentes React: un fichero = una responsabilidad
- Tests con Vitest, no Jest
- Nombres de funciones en inglés, comentarios en español
- Nunca hardcodear URLs — usar variables de entorno
```

Los ficheros de steering tienen cuatro modos de activación:

| Tipo | Front-matter | Cuándo se carga |
|---|---|---|
| **Siempre activo** | *(por defecto)* | En cada interacción sin excepción |
| **Por patrón de fichero** | `inclusion: fileMatch` | Solo al trabajar con ficheros que coincidan |
| **Manual** | `inclusion: manual` | Tú lo activas con `#NombreDelFichero` en el chat |
| **Automático** | `inclusion: auto` | Kiro lo activa cuando detecta que es relevante |

> 💡 **Analogía:** Es como el manual de incorporación de la empresa. Nadie lo lee en cada reunión, pero todos lo tienen interiorizado.

---

### ⚡ Paso 2 — Hooks · `.kiro/hooks/*.json`

**Son automatizaciones que se disparan cuando ocurre un evento en el IDE.**

Funcionan como un *revisor senior trabajando en segundo plano*: cada vez que guardas un fichero, creas uno nuevo o terminas una tarea, Kiro puede ejecutar acciones automáticamente. No tienes que acordarte de correr el linter, actualizar los tests o escanear credenciales — los hooks lo hacen por ti.

**Estructura de un hook:**
```json
{
  "version": "v1",
  "hooks": [{
    "name": "Lint al guardar",
    "trigger": "PostFileSave",
    "matcher": "\\.(ts|tsx)$",
    "action": {
      "type": "command",
      "command": "npm run lint"
    }
  }]
}
```

Los eventos disponibles y sus casos de uso más habituales:

| Evento | Cuándo se dispara | Uso típico |
|---|---|---|
| `PostFileSave` | Al guardar un fichero | Linting, validación de estilo |
| `PostFileCreate` | Al crear un fichero nuevo | Verificar estructura, añadir boilerplate |
| `PostFileDelete` | Al borrar un fichero | Limpiar referencias huérfanas |
| `PreToolUse` | Antes de que Kiro use una herramienta | Control de acceso, escaneo de seguridad |
| `PostToolUse` | Después de que Kiro use una herramienta | Auditoría, logging |
| `PostTaskExec` | Al completar una tarea de la spec | Ejecutar tests automáticamente |
| `SessionStart` | Al iniciar una sesión | Cargar contexto, recordatorios |
| `UserPromptSubmit` | Al enviar un mensaje al agente | Validar el prompt antes de procesarlo |

Las acciones que puede ejecutar un hook son de dos tipos:
- **`command`** — ejecuta un comando de shell (linter, tests, scripts de seguridad...)
- **`agent`** — inyecta un prompt al agente IA (revisar estilo, verificar principios de diseño...)

> 💡 **Analogía:** Es como un CI/CD local que se ejecuta en tu máquina en tiempo real, no al hacer push.

---

### 🔌 Paso 3 — MCP · `.kiro/settings/mcp.json`

**Es el fichero que conecta Kiro con herramientas y servicios externos.**

MCP (Model Context Protocol) es un protocolo abierto creado por Anthropic que permite al agente usar capacidades que van más allá del sistema de ficheros: consultar bases de datos, llamar a APIs externas, leer documentación propietaria, interactuar con servicios cloud, etc.

Sin MCP, Kiro solo puede leer/escribir ficheros y ejecutar comandos del sistema. Con MCP, puede, por ejemplo, consultar directamente el esquema de tu base de datos antes de generar una migración, o leer la documentación oficial de AWS en tiempo real.

**Ejemplo — `mcp.json`:**
```json
{
  "mcpServers": {
    "aws-docs": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false
    }
  }
}
```

Casos de uso comunes:

| Servidor MCP | Para qué sirve |
|---|---|
| `aws-documentation` | Consultar docs de AWS en tiempo real |
| `postgresql` / `sqlite` | Leer esquemas de BD directamente |
| `github` | Gestionar PRs, issues y repos |
| `filesystem` extendido | Acceso a rutas fuera del workspace |
| Documentación interna | Conectar wikis o APIs propietarias del equipo |

> 💡 **Analogía:** Son como los plugins o integraciones del agente — amplían lo que puede "ver" y "hacer" más allá del código fuente.

---

### 🧩 Los tres en conjunto

```
┌─────────────────────────────────────────────────────────────┐
│                    PROYECTO CON KIRO                        │
│                                                             │
│  📌 STEERING          ⚡ HOOKS            🔌 MCP            │
│  "¿Cómo trabajamos?"  "¿Qué pasa auto-   "¿Con qué habla   │
│                        máticamente?"      el agente?"       │
│                                                             │
│  Manual de equipo     CI/CD local         Plugins/APIs      │
│  Convenciones         Calidad continua    Contexto externo  │
│  Tech stack           Tests, lint         BD, docs, cloud   │
└─────────────────────────────────────────────────────────────┘
```

Configurados los tres, Kiro tiene todo el contexto necesario para trabajar de forma coherente con tu proyecto desde el primer prompt de cada sesión.

---

## 🔄 Ciclo de Vida de una Spec

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Prompt : Desarrollador\ndescribe idea

    Prompt --> Generando : Kiro analiza\ncodebase

    Generando --> EnRevision : Spec generada\n(3 documentos MD)

    EnRevision --> Aprobada : ✅ Desarrollador\naprueba

    EnRevision --> Editando : ✏️ Ajustes\nnecesarios

    Editando --> EnRevision : Kiro actualiza\ndocumentos

    Aprobada --> Implementando : Kiro ejecuta\ntareas

    Implementando --> Completada : ✅ Todas las tareas\nfinalizadas

    Implementando --> Actualizada : ⚠️ Cambian\nrequisitos

    Actualizada --> Implementando : Solo tareas\nafectadas

    Completada --> [*] : Feature en\nproducción
```

---

## ⚡ Sistema de Hooks — Cuándo se disparan

```mermaid
sequenceDiagram
    actor Dev as 👨‍💻 Desarrollador
    participant IDE as 🖥️ Kiro IDE
    participant Hook as ⚡ Hook Engine
    participant Agent as 🤖 Agente IA

    Dev->>IDE: Guarda fichero .tsx
    IDE->>Hook: Evento: PostFileSave
    Hook->>Hook: Matcher: \.(tsx|jsx)$
    Hook->>Agent: Ejecutar prompt:\n"Verifica SRP"
    Agent->>IDE: 💬 Feedback al desarrollador

    Dev->>IDE: Crea nueva función
    IDE->>Hook: Evento: PostFileCreate
    Hook->>Hook: Matcher: \.py$
    Hook->>Agent: Comando: run linter\n+ type checker
    Agent->>Dev: ⚠️ Avisos de calidad

    Dev->>IDE: Intenta hacer commit
    IDE->>Hook: Evento: PreToolUse
    Hook->>Hook: Matcher: execute_pwsh
    Hook->>Agent: Comando: git secrets --scan
    Agent-->>IDE: ❌ Credencial detectada\n[BLOQUEO]
    IDE->>Dev: 🚨 Commit bloqueado

    Dev->>IDE: Completa una tarea de la spec
    IDE->>Hook: Evento: PostTaskExec
    Hook->>Agent: Comando: npm run test
    Agent->>Dev: ✅ Tests pasados
```

---

## 🧭 ¿Cuándo usar cada modo?

```mermaid
flowchart LR
    START([Inicio de tarea]) --> Q1

    Q1{¿Funcionalidad\nnueva compleja?}
    Q1 -- Sí --> SPEC_MODE

    Q1 -- No --> Q2{¿Bugfix puntual\no refactor simple?}
    Q2 -- Sí --> VIBE_MODE
    Q2 -- No --> Q3{¿Varios\ndesarrolladores\nimplicados?}
    Q3 -- Sí --> SPEC_MODE
    Q3 -- No --> Q4{¿Necesitas\ntrazabilidad\nou auditoría?}
    Q4 -- Sí --> SPEC_MODE
    Q4 -- No --> VIBE_MODE

    subgraph SPEC_MODE ["📋 Modo SPEC"]
        S1[Spec Session] --> S2[Autopilot o Supervised]
        S2 --> S3["✅ requirements.md\n✅ design.md\n✅ tasks.md"]
    end

    subgraph VIBE_MODE ["💬 Modo VIBE"]
        V1[Vibe Session] --> V2[Chat directo\ncon el agente]
        V2 --> V3["⚡ Cambios rápidos\nsin especificación formal"]
    end

    style SPEC_MODE fill:#1a3a2a,color:#fff,stroke:#4ade80
    style VIBE_MODE fill:#1e3a5f,color:#fff,stroke:#4a9eff
```

---

## 🏗️ Capas de Contexto del Agente

```mermaid
graph TB
    subgraph CONTEXT ["🧠 Contexto del Agente Kiro"]
        direction TB

        L1["🌐 CAPA 1 — Conocimiento base del LLM\nLenguajes, frameworks, buenas prácticas generales"]

        L2["📌 CAPA 2 — Steering files del proyecto\n.kiro/steering/*.md\nConvenciones, tech stack, contexto de negocio"]

        L3["📋 CAPA 3 — Spec activa\nrequirements.md + design.md + tasks.md\nObjetivo concreto de la sesión actual"]

        L4["💬 CAPA 4 — Conversación de la sesión\nPrompts del desarrollador, historial reciente"]

        L5["🔍 CAPA 5 — Código fuente del proyecto\nFicheros relevantes del workspace"]

        L1 --> L2 --> L3 --> L4 --> L5
    end

    NOTE["💡 Las capas superiores tienen\nprioridad sobre las inferiores.\nEl steering siempre supera\nal conocimiento base del LLM."]

    CONTEXT --> NOTE

    style L1 fill:#2d2d2d,color:#aaa,stroke:#555
    style L2 fill:#1e3a5f,color:#fff,stroke:#4a9eff
    style L3 fill:#1a3a2a,color:#fff,stroke:#4ade80
    style L4 fill:#3a2a1a,color:#fff,stroke:#fb923c
    style L5 fill:#2a1a3a,color:#fff,stroke:#c084fc
    style NOTE fill:#1a1a2e,color:#ccc,stroke:#666
```

---

## 📊 Comparativa: SDD vs. Desarrollo tradicional con IA

```mermaid
timeline
    title Línea de tiempo: Feature nueva (estimación 1 semana)

    section Kiro SDD
        Día 1 : Configurar Steering y Hooks (1 vez)
              : Redactar prompt de intención (5 min)
              : Kiro genera Spec completa (automático)
        Día 1-2 : Revisión y aprobación de la Spec
                : Ajustes en requirements.md / design.md
        Día 2-5 : Implementación guiada por Spec
                : Hooks verifican calidad en tiempo real
                : Tasks completadas con trazabilidad total
        Día 5 : Documentación = la Spec misma
              : Zero deuda técnica de documentación

    section IA Tradicional (Cursor / Copilot)
        Día 1 : Prompt inicial → código generado
              : "En realidad quería decir..." x5
              : Contexto saturado de conversación
        Día 2-3 : Código válido pero con asunciones incorrectas
                : Refactorizar para encajar con convenciones
        Día 3-5 : Más prompts para cubrir casos no previstos
                : Depurar comportamientos inesperados
        Día 5+ : Escribir documentación desde cero
               : Deuda técnica acumulada
```

---

## ✅ Checklist del Flujo Óptimo

```mermaid
graph LR
    subgraph SETUP ["⚙️ Setup (solo 1 vez por proyecto)"]
        C1["☐ Crear .kiro/steering/conventions.md\ncon normas de código del equipo"]
        C2["☐ Crear .kiro/steering/tech-stack.md\ncon librerías y patrones"]
        C3["☐ Definir hooks de calidad\n(lint, tests, seguridad)"]
        C4["☐ Conectar MCPs necesarios\n(BD, APIs, docs externas)"]
    end

    subgraph PER_FEATURE ["🔁 Por cada funcionalidad"]
        C5["☐ Abrir sesión en modo Spec"]
        C6["☐ Redactar intención clara\n(qué, no cómo)"]
        C7["☐ Revisar requirements.md\n¿Cubre todos los casos?"]
        C8["☐ Revisar design.md\n¿Arquitectura coherente?"]
        C9["☐ Revisar tasks.md\n¿Orden y dependencias OK?"]
        C10["☐ Elegir Autopilot o Supervised\nsegún la criticidad"]
        C11["☐ Ejecutar tareas\nuna a una o en bloque"]
        C12["☐ Verificar que los hooks\nno reportan errores"]
    end

    SETUP --> PER_FEATURE

    style SETUP fill:#1e3a5f,color:#fff,stroke:#4a9eff
    style PER_FEATURE fill:#1a3a2a,color:#fff,stroke:#4ade80
```

---

## 🔗 Referencias

| Recurso | Enlace |
|---|---|
| Documentación oficial | [kiro.dev/docs](https://kiro.dev/docs/) |
| Introducción a Kiro | [kiro.dev/blog/introducing-kiro](https://kiro.dev/blog/introducing-kiro/) |
| Deep dive: de chat a specs | [kiro.dev/blog/from-chat-to-specs-deep-dive](https://kiro.dev/blog/from-chat-to-specs-deep-dive/) |
| Guía completa SDD 2026 | [pingax.com/kiro-spec-driven-development](https://pingax.com/kiro-spec-driven-development/) |
| Repositorio oficial | [github.com/kirodotdev/Kiro](https://github.com/kirodotdev/Kiro) |

---
