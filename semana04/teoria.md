# Semana 4 — Teoría: LangGraph y pipelines multi-agente

## Agente vs Pipeline multi-agente

En semana 3 un solo agente ReAct decidía qué tools usar. El problema: todo el razonamiento cae sobre un solo LLM sin estructura.

Un **pipeline multi-agente** divide el problema en agentes especializados, cada uno con un rol claro:

```
Semana 3:  un agente generalista que decide qué tool usar
Semana 4:  varios agentes especializados coordinados en secuencia
```

### Analogía con embebidos

```
Agente único  =  una función monolítica que hace todo
                 void process(void) { analiza + detecta + corrige }

Multi-agente  =  tareas separadas en RTOS, cada una con su responsabilidad
                 task_analizar()  → task_detectar() → task_mejorar()
                 con cola de mensajes entre ellas (el estado compartido)
```

---

## LangGraph — qué es y por qué existe

LangGraph es una librería que permite construir flujos de trabajo con agentes como **grafos con estado**.

Problema que resuelve: LangChain chains son lineales y sin memoria entre pasos. LangGraph agrega:

1. **Estado compartido** — todos los nodos leen y escriben en un mismo diccionario
2. **Grafos** — puedes definir cualquier topología: secuencial, paralela, condicional
3. **Control explícito** — tú defines cuándo termina el grafo (`END`)

---

## StateGraph — el componente central

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class EstadoRevision(TypedDict):
    codigo: str
    analisis: str
    errores: str
    mejoras: str

grafo = StateGraph(EstadoRevision)
```

`TypedDict` define las claves del estado. Cada nodo puede leer cualquier clave y actualizar solo las que modifica — el resto se conserva automáticamente.

---

## Nodos

Un nodo es una función Python que recibe el estado actual y retorna un dict con las claves que modifica:

```python
def nodo_analizar(estado: EstadoRevision) -> dict:
    # lee del estado
    codigo = estado["codigo"]
    # llama al LLM
    resultado = chain.invoke({"codigo": codigo})
    # solo retorna la clave que modifica
    return {"analisis": resultado}
```

El nodo no necesita retornar el estado completo — LangGraph hace el merge automáticamente.

---

## Edges (aristas)

Los edges definen el flujo entre nodos:

```python
grafo.set_entry_point("analizar")          # nodo inicial
grafo.add_edge("analizar", "detectar_errores")
grafo.add_edge("detectar_errores", "mejorar")
grafo.add_edge("mejorar", END)             # termina el grafo
```

### Tipos de edges

| Tipo | Cómo se define | Cuándo usarlo |
|------|----------------|---------------|
| Secuencial | `add_edge(A, B)` | El nodo B siempre ejecuta después de A |
| Condicional | `add_conditional_edges(A, fn)` | La función `fn` decide el siguiente nodo |
| Paralelo | múltiples edges desde un nodo | A dispara B y C al mismo tiempo |

En semana 4 usamos solo edges secuenciales — es la topología más simple.

---

## Flujo de datos entre nodos

El estado compartido es lo que conecta los agentes. Cada nodo recibe el contexto acumulado de los anteriores:

```
Estado inicial:   { codigo: "...", analisis: "", errores: "", mejoras: "" }
                              ↓
nodo_analizar:    lee [codigo]        → escribe [analisis]
                              ↓
nodo_detectar:    lee [codigo, analisis]   → escribe [errores]
                              ↓
nodo_mejorar:     lee [codigo, analisis, errores]  → escribe [mejoras]
                              ↓
Estado final:     { codigo: "...", analisis: "...", errores: "...", mejoras: "..." }
```

El Agente 2 no reanaliza el código desde cero — parte del análisis del Agente 1. El Agente 3 conoce tanto el análisis como los errores. Eso es la ventaja del estado compartido.

---

## Comparación con chains de semana 2

| | Chain LCEL (semana 2) | StateGraph (semana 4) |
|---|---|---|
| **Estructura** | `A | B | C` — la salida de A es la entrada de B | Nodos independientes con estado compartido |
| **Estado** | No existe — cada paso solo ve la salida del anterior | Diccionario tipado accesible por todos |
| **Ramificación** | No soportada directamente | `add_conditional_edges` nativo |
| **Especialización** | Un chain hace todo | Cada nodo tiene su propio prompt/rol |
| **Extensibilidad** | Agregar un paso rompe la cadena | Agregar un nodo no afecta los demás |

---

## Evolución a través de las semanas

```
Semana 1:  llamada directa a la API             → respuesta fija, sin estructura
Semana 2:  chain LCEL                           → flujo predefinido, reutilizable
Semana 3:  agente ReAct + tools                 → flujo dinámico, herramientas externas
Semana 4:  LangGraph multi-agente               → agentes especializados, estado compartido
```

---

## Por qué importa para el Proyecto 1 (RAG Chatbot)

El RAG Chatbot necesitará al menos dos etapas: recuperar contexto del datasheet y generar la respuesta. Con LangGraph esas etapas son nodos separados con estado compartido:

```
[nodo_recuperar]  → busca en el datasheet STM32F407
        ↓ estado: { pregunta, fragmentos_recuperados }
[nodo_responder]  → genera respuesta con el contexto recuperado
        ↓
respuesta final
```

Lo que construyes esta semana es exactamente esa estructura base.
