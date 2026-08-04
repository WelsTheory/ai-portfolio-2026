# Glosario — AI Portfolio

Términos ordenados alfabéticamente. Cada entrada incluye una definición breve y un ejemplo concreto del contexto del proyecto.

---

## A

### API (Application Programming Interface)
**Definición:** Interfaz que permite a dos programas comunicarse entre sí. En el contexto de LLMs, es el punto de acceso al modelo que corre en los servidores del proveedor.

**Ejemplo:**
```python
client = anthropic.Anthropic()
client.messages.create(...)   # llamada a la API de Anthropic
```

---

### Alucinación
**Definición:** Cuando un LLM genera texto que suena convincente pero es factualmente incorrecto. El modelo no "sabe" que está equivocado — simplemente predice el token más probable.

**Ejemplo:** En semana 1, el modelo local afirmó que el STM32F407 tiene 7 canales DMA. La cifra correcta es 16 streams. El modelo generó una respuesta plausible, no una verdadera.

---

## C

### Chain (cadena)
**Definición:** Secuencia de componentes conectados donde la salida de uno es la entrada del siguiente. Concepto central de LangChain.

**Ejemplo:**
```python
chain = prompt | llm | parser
# prompt genera el mensaje → llm lo procesa → parser extrae el texto
```

---

### Context Window (ventana de contexto)
**Definición:** Límite máximo de tokens que un modelo puede procesar en una sola llamada, incluyendo el prompt y la respuesta. Si el texto supera este límite, el modelo no puede "ver" lo que quedó fuera.

**Ejemplo:** Claude Haiku tiene una ventana de contexto de 200 000 tokens. Si mandas un datasheet de 300 páginas, cabe. Si mandas varios datasheets a la vez, puede no caber.

---

## E

### Embedding
**Definición:** Representación numérica (vector) de un texto. Palabras con significado similar quedan cerca en el espacio vectorial. Permite buscar por significado, no solo por palabras exactas.

**Ejemplo:**
```
"timer"    → [0.21, -0.83, 0.44, ...]
"counter"  → [0.19, -0.79, 0.41, ...]   ← cerca: significado similar
"FreeRTOS" → [0.67,  0.12, -0.55, ...]  ← lejos: concepto diferente
```

---

## L

### LCEL (LangChain Expression Language)
**Definición:** Sintaxis de LangChain que usa el operador `|` para encadenar componentes de forma legible y declarativa.

**Ejemplo:**
```python
# En lugar de esto:
parsed = parser.invoke(llm.invoke(prompt.invoke({"topic": "DMA"})))

# Escribes esto:
chain = prompt | llm | parser
parsed = chain.invoke({"topic": "DMA"})
```

---

### LLM (Large Language Model)
**Definición:** Modelo de inteligencia artificial entrenado con grandes volúmenes de texto para predecir el siguiente token. La predicción encadenada genera respuestas coherentes.

**Ejemplo:** Claude Haiku, GPT-4, Llama 3, Qwen2.5 son todos LLMs. En semana 1 usamos `claude-haiku-4-5-20251001` via API y un modelo local via LM Studio.

---

## M

### max_tokens
**Definición:** Parámetro que limita cuántos tokens puede generar el modelo en su respuesta. No afecta el prompt, solo la salida.

**Ejemplo:** Con `max_tokens=512`, la respuesta sobre DMA en semana 1 se cortó antes de completar el ejemplo de código C. Subir a `max_tokens=1024` hubiera dado la respuesta completa.

---

### Messages
**Definición:** Lista de turnos de conversación que se envía a la API en cada llamada. Como la API es stateless, debes enviar el historial completo cada vez.

**Ejemplo:**
```python
messages=[
    {"role": "user",      "content": "¿Qué es el DMA?"},
    {"role": "assistant", "content": "El DMA es..."},
    {"role": "user",      "content": "¿Y cuándo uso interrupciones?"},
]
```

---

### Modelo local
**Definición:** LLM que corre en tu propia máquina, sin enviar datos a servidores externos. Requiere más RAM pero garantiza privacidad y tiene costo cero por token.

**Ejemplo:** En semana 1 usamos LM Studio en `http://localhost:1234/v1` para correr un modelo GGUF localmente, usando el mismo cliente `openai` que en la nube.

---

## O

### OutputParser
**Definición:** Componente de LangChain que transforma la respuesta del LLM al formato que necesita tu aplicación.

**Ejemplo:**
```python
StrOutputParser()     # → str   (texto plano)
JsonOutputParser()    # → dict  (diccionario Python)
PydanticOutputParser  # → objeto validado con tipos definidos
```

---

## P

### Prompt
**Definición:** El texto de entrada que le envías al modelo. Es la instrucción, pregunta o contexto que define qué quieres que el modelo haga.

**Ejemplo:** `"Soy ingeniero electrónico trabajando con STM32F407. Explícame brevemente cómo funciona el DMA..."` — ese es el prompt de semana 1.

---

### PromptTemplate
**Definición:** Plantilla de prompt con variables que se rellenan en tiempo de ejecución. Permite reutilizar el mismo prompt con distintos inputs.

**Ejemplo:**
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en STM32."),
    ("human",  "Explícame brevemente: {topic}"),   # {topic} es la variable
])
prompt.invoke({"topic": "DMA"})     # genera el mensaje completo
prompt.invoke({"topic": "UART"})    # mismo template, distinto input
```

---

### Pydantic
**Definición:** Librería Python para definir esquemas de datos con tipos y validación. En LangChain se usa para forzar al modelo a devolver JSON con campos específicos.

**Ejemplo:**
```python
class AnalisisPeriferico(BaseModel):
    nombre: str
    casos_dma: list[str]
    nivel_complejidad: str   # el modelo DEBE devolver estos campos

llm.with_structured_output(AnalisisPeriferico)
```

---

## R

### RAG (Retrieval-Augmented Generation)
**Definición:** Técnica que combina búsqueda en una base de conocimiento propia con generación del LLM. El modelo responde basándose en documentos reales, reduciendo alucinaciones.

**Ejemplo:** El Proyecto 1 del portfolio es un RAG: el usuario pregunta sobre un datasheet STM32, el sistema busca los fragmentos relevantes en ChromaDB y Claude los usa para responder con precisión.

---

## S

### Stateless
**Definición:** La API no guarda memoria entre llamadas. Cada request es independiente y debes enviar el historial completo si quieres que el modelo recuerde la conversación.

**Ejemplo:** Si en la llamada 1 preguntas "¿Qué es DMA?" y en la llamada 2 preguntas "¿Y cuántos streams tiene?", el modelo no sabrá a qué te refieres con "streams" a menos que incluyas el turno anterior en `messages`.

---

### Structured Output
**Definición:** Respuesta del LLM en un formato estructurado y validado (JSON, objeto Pydantic) en lugar de texto libre. Hace la salida predecible y directamente usable en código.

**Ejemplo:** En `chain_json.py` de semana 2, en lugar de texto libre obtenemos:
```python
AnalisisPeriferico(
    nombre="UART1",
    casos_dma=["recibir 100+ bytes", "streaming continuo"],
    nivel_complejidad="Media"
)
```

---

## T

### Token
**Definición:** Unidad mínima de texto que procesa un LLM. No es una letra ni una palabra completa — es un fragmento intermedio. El costo de la API se mide en tokens.

**Ejemplo:**
```
"STM32F407" → ["ST", "M", "32", "F", "407"]   # ~5 tokens
"DMA"       → ["DMA"]                           # 1 token
"HAL_UART_Receive_DMA" → ~6 tokens
```
Regla práctica: **1 token ≈ 0.75 palabras en inglés**.

---

### Tokenización
**Definición:** Proceso de convertir texto en tokens antes de enviarlo al modelo. El modelo nunca ve texto — solo ve secuencias de IDs numéricos.

**Ejemplo:**
```
"Hola mundo" → [15496, 14056]   # IDs internos del vocabulario del modelo
```

---

### Transformer
**Definición:** Arquitectura de red neuronal base de todos los LLMs modernos. Su innovación clave es el mecanismo de **atención**: procesa todos los tokens en paralelo y calcula cuánta relevancia tiene cada token para cada otro.

**Ejemplo:** Cuando escribes "El DMA transfiere datos sin intervención del **CPU**", el Transformer entiende que "CPU" está relacionado con "DMA" y "transfiere" gracias a la atención — no porque estén adyacentes, sino porque aprendió esa relación durante el entrenamiento.

---

*Glosario en construcción — se actualiza cada semana.*
