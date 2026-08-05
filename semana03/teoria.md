# Semana 3 — Teoría: Agentes y ReAct

## Chain vs Agente — la diferencia clave

En semana 2 construiste chains: flujos **fijos** donde los pasos están predefinidos.

```
chain_basica:  prompt → llm → parser   (siempre los mismos pasos)
```

Un **agente** decide en tiempo de ejecución qué pasos ejecutar y cuántas veces:

```
agente: llm decide → usar tool? → observar resultado → decidir otra vez → respuesta final
```

### Analogía: chain vs agente en embebidos

```
Chain   = función determinista en C
          calcular_baud_rate(fclk, baudrate) → siempre el mismo flujo

Agente  = sistema con lógica de decisión (como un RTOS con tareas)
          el LLM evalúa la situación y decide qué "tarea" ejecutar
```

---

## ReAct — Reason + Act

ReAct es el patrón más común para agentes. El modelo alterna entre:

1. **Thought** — razona sobre qué necesita hacer
2. **Action** — elige una tool y sus parámetros
3. **Observation** — recibe el resultado de la tool
4. Repite hasta tener respuesta final

```
Pregunta: ¿Qué prescaler necesito para TIM2 a 1kHz con ARR=999?

Thought:  Necesito calcular el prescaler. Tengo la herramienta calcular_prescaler.
Action:   calcular_prescaler
Input:    {"fclk_mhz": 84, "frecuencia_hz": 1000, "arr": 999}
Obs:      PSC = 83 (para ARR=999, 1000Hz con FCLK=84MHz)

Thought:  Ya tengo el resultado.
Final:    El prescaler para TIM2 es PSC=83 con ARR=999.
```

El LLM actúa como el "cerebro" que decide cuándo y cómo usar cada herramienta.

---

## Tools (herramientas)

Una tool es cualquier función Python que el agente puede llamar. Se declaran con el decorador `@tool`:

```python
from langchain_core.tools import tool

@tool
def calcular_baudrate(fclk_mhz: float, baudrate: int) -> str:
    """Calcula el valor BRR para configurar UART en STM32."""
    brr = fclk_mhz * 1_000_000 / (16 * baudrate)
    ...
```

El docstring es crítico — el agente lo lee para saber cuándo usar cada tool.

### Tipos de tools

| Tipo | Ejemplo | Cuándo usarlo |
|------|---------|---------------|
| Cálculo | `calcular_baudrate()` | Operaciones matemáticas exactas |
| Búsqueda | `buscar_datasheet()` | Recuperar información externa |
| API externa | `leer_sensor()` | Interactuar con sistemas reales |
| Base de datos | `consultar_periferico()` | Lookup en datos estructurados |

---

## AgentExecutor

El `AgentExecutor` es el loop que ejecuta el ciclo ReAct:

```python
from langchain.agents import create_react_agent, AgentExecutor

agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

resultado = executor.invoke({"input": "¿Cuál es el BRR para 115200 baud?"})
```

Con `verbose=True` puedes ver cada paso del razonamiento en consola — útil para entender qué está haciendo el agente.

---

## Evolución a través de las semanas

```
Semana 1:  llamada directa a la API         → respuesta fija
Semana 2:  chain LCEL                       → flujo predefinido, reutilizable
Semana 3:  agente ReAct + tools             → flujo dinámico, puede calcular y buscar
Semana 4:  LangGraph multi-agente           → múltiples agentes coordinados
```

---

## Por qué importa para el Proyecto 1 (RAG Chatbot)

En el RAG Chatbot el agente tendrá una tool de búsqueda en el datasheet:

```
Pregunta: "¿Cuál es el voltaje máximo de los pines GPIO del STM32F407?"
    ↓
Thought: Necesito buscar en el datasheet
Action: buscar_en_datasheet(query="GPIO voltaje máximo")
Obs:    "VDD + 0.3V, máximo 4.0V según tabla 14..."
    ↓
Final: El voltaje máximo es VDD+0.3V (máx 4.0V)
```

Lo que construyes esta semana es exactamente ese mecanismo.
