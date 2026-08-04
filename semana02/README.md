# Semana 2 — LangChain + LCEL

## Scripts

| Script | Descripción |
|--------|-------------|
| `chain_basica.py` | PromptTemplate → ChatAnthropic → StrOutputParser |
| `chain_json.py` | PromptTemplate → ChatAnthropic → Pydantic (structured output) |

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

## Cómo correr

```bash
# Windows (PowerShell)
.venv\Scripts\activate
python semana02/chain_basica.py
python semana02/chain_json.py

# Linux / macOS
source .venv/bin/activate
python semana02/chain_basica.py
python semana02/chain_json.py
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

---

## Qué sigue

En **Semana 3** los chains se convierten en agentes con `ReAct`:
`chain → AgentExecutor → tools (búsqueda, calculadora, datasheet lookup)`
