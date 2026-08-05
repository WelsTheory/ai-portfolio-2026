# Semana 2 — Teoría: LangChain y LCEL

## ¿Qué es LangChain?

LangChain es un framework para construir aplicaciones con LLMs. Su valor no está en llamar al modelo (eso ya lo hacías en Semana 1), sino en **encadenar** operaciones de forma declarativa y reutilizable.

### Analogía: LangChain es el HAL de los LLMs

En STM32 usas HAL para no escribir registros directamente:

```c
// Sin HAL — específico del hardware
USART2->DR = data;

// Con HAL — abstracto, portable entre micros
HAL_UART_Transmit(&huart2, &data, 1, 100);
```

LangChain hace lo mismo con los LLMs:

```python
# Sin LangChain — específico de Anthropic (Semana 1)
client = anthropic.Anthropic()
message = client.messages.create(...)
texto = message.content[0].text

# Con LangChain — abstracto, portable entre proveedores (Semana 2)
llm = ChatAnthropic(...)
result = llm.invoke(prompt)
```

La ventaja: en `chain_mistral.py` solo se cambió `ChatAnthropic` por `ChatMistralAI` y todo lo demás funcionó igual — igual que portar código HAL de STM32F4 a STM32H7.

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

### Analogía: LCEL es un pipeline de señal DSP

En procesamiento de señal encadenas bloques donde la salida de uno es la entrada del siguiente:

```
Sensor → Filtro → Amplificador → ADC → Buffer
```

LCEL es lo mismo pero para texto:

```python
chain = prompt | llm | parser
#       ↓         ↓      ↓
#   formatea   procesa  extrae
#   el texto   con IA   el string
```

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

### Analogía: Pydantic es un struct de C

Definir la clase en Python es lo mismo que definir un `struct` en C — le dices al modelo exactamente qué campos debe rellenar y con qué tipo:

```c
// C — defines el contrato de datos
typedef struct {
    char  nombre[20];
    char  descripcion[200];
    char  casos_dma[5][100];
    char  casos_interrupcion[5][100];
    char  funcion_hal_ejemplo[50];
    char  nivel_complejidad[10];   // "Baja" | "Media" | "Alta"
} AnalisisPeriferico;
```

```python
# Python — mismo concepto con validación automática
class AnalisisPeriferico(BaseModel):
    nombre: str
    descripcion: str
    casos_dma: list[str]
    casos_interrupcion: list[str]
    funcion_hal_ejemplo: str
    nivel_complejidad: str         # "Baja" | "Media" | "Alta"
```

El modelo no devuelve texto libre — devuelve un objeto que cumple ese contrato. Por eso puedes acceder a `resultado.nombre` o `resultado.casos_dma` directamente, igual que a los campos de un struct.

**La diferencia práctica:**

```python
# chain_basica → texto, solo sirve para leer
"UART1 tiene complejidad media y conviene usar DMA cuando..."

# chain_json → objeto, puedes usarlo en lógica de código
if resultado.nivel_complejidad == "Alta":
    print("Cuidado, configuración compleja")

for caso in resultado.casos_dma:
    guardar_en_base_de_datos(caso)
```

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
