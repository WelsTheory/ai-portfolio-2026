# Semana 1 — Primera llamada a Claude API y modelos locales

## Scripts

| Script | Proveedor | Descripción |
|--------|-----------|-------------|
| `hello_claude.py` | Claude API | Primera llamada a Anthropic, respuesta sobre STM32F407 |
| `hello_local.py` | LM Studio (local) | Misma pregunta usando un modelo local vía LM Studio |
| `multi_provider.py` | Claude + Local | Compara la respuesta de ambos proveedores lado a lado |

---

## `hello_claude.py`

```
.env (ANTHROPIC_API_KEY)
    ↓
anthropic.Anthropic()       ← cliente autenticado
    ↓
client.messages.create()    ← envía el mensaje
    ↓
message.content[0].text     ← extrae el texto
    ↓
print()
```

### Parámetros importantes

| Parámetro | Valor | Qué controla |
|-----------|-------|--------------|
| `model` | `claude-haiku-4-5-20251001` | Modelo más rápido y barato — ideal para pruebas |
| `max_tokens` | `512` | Límite de tokens en la respuesta |
| `messages` | lista de `role` + `content` | El historial de conversación |

---

## `hello_local.py`

LM Studio expone una API compatible con OpenAI en `http://localhost:1234/v1`. Esto permite usar el mismo cliente (`openai`) para cualquier modelo local cargado en LM Studio (Qwen3, Llama, etc.).

```
LM Studio corriendo con modelo cargado
    ↓
OpenAI(base_url="http://localhost:1234/v1")   ← apunta al servidor local
    ↓
client.chat.completions.create()
    ↓
response.choices[0].message.content
```

> Antes de correr este script, asegúrate de tener LM Studio abierto con un modelo cargado.

---

## `multi_provider.py`

Llama a ambos proveedores con la misma pregunta y muestra las respuestas en paralelo. Útil para comparar calidad, velocidad y estilo de respuesta entre modelos.

```
misma pregunta
    ├── ask_claude()  → Claude Haiku (API remota)
    └── ask_local()   → LM Studio   (localhost)
            ↓
    print lado a lado
```

---

## Por qué `messages` es una lista

La API es stateless — no recuerda conversaciones anteriores. Cada llamada envía el historial completo. Más adelante (Semana 2) esto importa cuando construyamos cadenas con LangChain.

---

## Cómo correr cada script

```bash
# Windows (PowerShell) — desde la raíz del proyecto
.venv\Scripts\activate
python semana01/hello_claude.py      # solo Claude API
python semana01/hello_local.py       # solo modelo local (LM Studio debe estar abierto)
python semana01/multi_provider.py    # comparación lado a lado

# Linux / macOS — desde la raíz del proyecto
source .venv/bin/activate
python semana01/hello_claude.py
python semana01/hello_local.py
python semana01/multi_provider.py
```

## Requisito adicional

`hello_local.py` y `multi_provider.py` usan el paquete `openai`:

```powershell
pip install openai
```

---

## Qué sigue

En **Semana 2** esto evoluciona a una chain con LangChain:  
`prompt template → LLM → output parser → JSON estructurado`
