# Semana 2 — LangChain + LCEL

## Scripts

| Script | Proveedor | Costo | Descripción |
|--------|-----------|-------|-------------|
| `chain_basica.py` | Claude (Anthropic) | Pago | PromptTemplate → ChatAnthropic → StrOutputParser |
| `chain_mistral.py` | Mistral | **Gratis** | Mismo chain que arriba usando Mistral |
| `chain_json.py` | Claude (Anthropic) | Pago | PromptTemplate → ChatAnthropic → Pydantic (structured output) |
| `chain_historial.py` | Claude (Anthropic) | Pago | Conversación con historial entre turnos |

---

## `chain_basica.py`

Evolución directa de `hello_claude.py`: el prompt ya no es texto fijo sino un template con variable `{topic}`.

```
{"topic": "DMA"}
    ↓ ChatPromptTemplate     ← formatea el mensaje con system + human
    ↓ ChatAnthropic          ← llama a la API
    ↓ StrOutputParser        ← extrae el texto del AIMessage
    ↓ str
```

### LCEL — pipe syntax

```python
chain = prompt | llm | parser
result = chain.invoke({"topic": "DMA controller"})
```

El operador `|` encadena componentes. Es equivalente a:

```python
result = parser.invoke(llm.invoke(prompt.invoke({"topic": "DMA controller"})))
```

---

## `chain_mistral.py` — versión gratuita

Exactamente el mismo chain que `chain_basica.py`, solo cambia el modelo por `ChatMistralAI`. Útil para quienes no tienen API key de Anthropic.

```python
# chain_basica.py
llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

# chain_mistral.py
llm = ChatMistralAI(model="mistral-small-latest")

# El chain es idéntico en ambos:
chain = prompt | llm | parser
```

> Esto demuestra una ventaja clave de LangChain: puedes cambiar el modelo sin tocar el resto del código.

---

## `chain_json.py`

En lugar de devolver texto libre, la chain devuelve un **objeto Python validado** con Pydantic.

```
{"periferico": "UART1"}
    ↓ ChatPromptTemplate
    ↓ ChatAnthropic.with_structured_output(AnalisisPeriferico)
    ↓ AnalisisPeriferico (objeto Pydantic)
```

### Esquema `AnalisisPeriferico`

```python
class AnalisisPeriferico(BaseModel):
    nombre: str
    descripcion: str
    casos_dma: list[str]
    casos_interrupcion: list[str]
    funcion_hal_ejemplo: str
    nivel_complejidad: str          # "Baja" | "Media" | "Alta"
```

`with_structured_output()` instruye al modelo a devolver siempre ese esquema. Si el modelo no puede cumplirlo, lanza una excepción — más robusto que parsear texto libre.

---

## `chain_historial.py`

Muestra cómo el modelo puede "recordar" una conversación enviando el historial completo en cada llamada.

```
historial = [SystemMessage]
    ↓
turno 1: historial += [HumanMessage] → llm.invoke(historial) → AIMessage
turno 2: historial += [HumanMessage] → llm.invoke(historial) → AIMessage
turno 3: ...
```

Conecta directamente con el concepto de semana 1: **la API es stateless**, pero si acumulamos los mensajes anteriores y los enviamos en cada llamada, el modelo tiene contexto completo.

### Conversación de ejemplo

```
[1] ¿Cómo funciona el DMA controller del STM32F407?
[2] ¿Y cuántos streams tiene en total?          ← no necesita repetir "DMA"
[3] ¿Cuál usarías para recibir datos de UART1?  ← el modelo recuerda el contexto
[4] Dame un ejemplo de código HAL para eso.
```

---

## Cómo correr

```bash
# Windows (PowerShell)
.venv\Scripts\activate
python semana02/chain_basica.py       # requiere ANTHROPIC_API_KEY
python semana02/chain_mistral.py      # requiere MISTRAL_API_KEY
python semana02/chain_json.py         # requiere ANTHROPIC_API_KEY
python semana02/chain_historial.py    # requiere ANTHROPIC_API_KEY

# Linux / macOS
source .venv/bin/activate
python semana02/chain_basica.py
python semana02/chain_mistral.py
python semana02/chain_json.py
python semana02/chain_historial.py
```

### Dependencia adicional para `chain_mistral.py`

```bash
pip install langchain-mistralai
```

---

## Diferencia clave respecto a Semana 1

| | Semana 1 | Semana 2 |
|---|---|---|
| **Prompt** | String fijo | Template con variables |
| **Cliente** | `anthropic.Anthropic()` directo | `ChatAnthropic` (LangChain) |
| **Salida** | `message.content[0].text` | `StrOutputParser` o Pydantic |
| **Composición** | Llamadas manuales | Pipe `\|` (LCEL) |
| **Reutilización** | Copiar y pegar | `chain.invoke({...})` con distintos inputs |
| **Cambiar modelo** | Reescribir el cliente | Cambiar solo `llm = ...` |
| **Historial** | Lista `messages` manual | `HumanMessage` / `AIMessage` acumulados |

---

## Qué sigue

En **Semana 3** los chains se convierten en agentes con `ReAct`:
`chain → AgentExecutor → tools (búsqueda, calculadora, datasheet lookup)`
