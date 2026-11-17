# Semana 4 — Conclusiones

## Qué se construyó

| Componente | Descripción |
|------------|-------------|
| `revisor_codigo.py` | Pipeline multi-agente con LangGraph — 3 nodos secuenciales |
| Agente 1 — Analizador | Describe qué hace el código C |
| Agente 2 — Detector | Encuentra errores HAL/STM32 con contexto del Agente 1 |
| Agente 3 — Mejorador | Sugiere mejoras con contexto de los dos anteriores |
| Reporte `.md` | Consolidado con los tres análisis y el código fuente |

---

## Observaciones

### Pipeline secuencial con estado compartido

- El estado `EstadoRevision` con `TypedDict` funcionó como se esperaba — cada nodo solo retorna las claves que modifica y LangGraph hace el merge.
- El Agente 2 recibió el análisis del Agente 1 correctamente como contexto adicional. Esto redujo descripciones redundantes: el detector no volvió a explicar qué hace el código, directamente señaló los errores.
- El Agente 3 mostró el mayor beneficio del estado compartido — sus mejoras fueron coherentes con los errores detectados por el Agente 2, sin repetir observaciones ya mencionadas.

### Código de ejemplo STM32

El código UART de ejemplo tiene errores reales y el pipeline los identificó correctamente:
- `HAL_UART_Init` sin verificación del valor de retorno
- `HAL_UART_Receive_IT` con buffer de 256 bytes en `main` (riesgo de overflow si se llama desde el callback)
- Callback sin validación de instancia (`huart->Instance != USART1`)
- Falta de `__HAL_RCC_USART1_CLK_ENABLE()` antes de `HAL_UART_Init`

### Tiempo de ejecución

Tres llamadas secuenciales al LLM significa tres veces la latencia. Para revisión de código no es un problema, pero para casos interactivos se debería considerar paralelización con edges múltiples.

---

## Diferencia clave vs Semana 3

| | Semana 3 (agente ReAct) | Semana 4 (LangGraph) |
|---|---|---|
| **Estructura** | Un agente decide dinámicamente | Flujo definido explícitamente |
| **Especialización** | El agente generalista hace todo | Cada nodo tiene prompt y rol específico |
| **Contexto entre pasos** | El historial del chat | Estado tipado y estructurado |
| **Debugging** | Leer el razonamiento del agente | Ver el estado en cada nodo |
| **Cuándo usarlo** | Tareas abiertas donde el flujo no se conoce | Pipelines donde los pasos están claros |

---

## Lo que aprendimos

| Concepto | Dónde se ve |
|----------|-------------|
| `StateGraph` con `TypedDict` | `EstadoRevision` — estado tipado accesible por todos los nodos |
| Nodos como funciones Python | `nodo_analizar`, `nodo_detectar_errores`, `nodo_mejorar` |
| Edges secuenciales | `add_edge` conecta los tres nodos en orden |
| Estado acumulativo | Cada nodo lee las claves escritas por los anteriores |
| Separación de responsabilidades | Tres prompts distintos, cada uno optimizado para su tarea |
| `set_entry_point` y `END` | Definen dónde empieza y termina el grafo |

---

## Limitación identificada

El Agente 2 recibe el código completo más el análisis — si el archivo C fuera muy largo, el contexto del prompt podría superar el `max_tokens=1024` del modelo. Para archivos grandes habría que chunking del código o aumentar el límite.
