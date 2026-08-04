# Semana 2 — Teoría: LangChain y LCEL

## ¿Qué es LangChain?

LangChain es un framework para construir aplicaciones con LLMs. Su valor no está en llamar al modelo (eso ya lo hacías en Semana 1), sino en **encadenar** operaciones de forma declarativa y reutilizable.

---

## LCEL — LangChain Expression Language

La forma moderna de construir chains en LangChain usa el operador `|` (pipe), igual que en Unix:

```python
chain = prompt | llm | output_parser
result = chain.invoke({"topic": "DMA"})
```

Cada componente recibe la salida del anterior. Es lo mismo que:

```python
output_parser.invoke(llm.invoke(prompt.invoke({"topic": "DMA"})))
```

pero legible y componible.

---

## Los 3 bloques de una chain básica

### 1. PromptTemplate
Convierte variables en un mensaje formateado:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en microcontroladores STM32."),
    ("human",  "Explícame brevemente: {topic}"),
])
```

**Ventaja vs Semana 1**: el prompt es un template reutilizable. Cambias `{topic}` y obtienes respuestas distintas sin reescribir nada.

### 2. ChatModel (LLM)
El modelo que procesa el prompt:

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)
```

LangChain abstrae el cliente: puedes cambiar `ChatAnthropic` por `ChatOpenAI` o `ChatOllama` sin tocar el resto de la chain.

### 3. OutputParser
Convierte la respuesta del LLM al formato que necesitas:

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
```

| Parser | Salida | Cuándo usarlo |
|--------|--------|---------------|
| `StrOutputParser` | `str` | Texto plano, Markdown |
| `JsonOutputParser` | `dict` | Cuando necesitas campos estructurados |
| `PydanticOutputParser` | objeto Python | Cuando necesitas validación de tipos |

---

## Flujo completo vs Semana 1

```
SEMANA 1 (raw SDK):
texto  →  client.messages.create()  →  message.content[0].text

SEMANA 2 (LCEL):
{"topic": "DMA"}  →  PromptTemplate  →  ChatAnthropic  →  OutputParser  →  resultado
```

---

## Structured Output con Pydantic

La forma más robusta de obtener JSON es definir el esquema con Pydantic y usar `with_structured_output()`:

```python
from pydantic import BaseModel

class AnalisisPeriferico(BaseModel):
    nombre: str
    descripcion: str
    usa_dma: bool
    funcion_hal: str

llm_structured = llm.with_structured_output(AnalisisPeriferico)
```

El modelo intentará siempre devolver un objeto que cumpla ese esquema. Si falla, lanza una excepción — mucho mejor que parsear texto libre.

---

## Por qué LCEL importa para los proyectos

En el **Proyecto 1 (RAG Chatbot)** la chain será:

```
pregunta
  → PromptTemplate (con contexto del datasheet)
  → ChatAnthropic
  → StrOutputParser
  → respuesta
```

Y en el **Proyecto 2 (Evaluación de Prompts)** necesitarás chains que devuelvan JSON para comparar estrategias. Lo que construyes esta semana es la base de ambos.
