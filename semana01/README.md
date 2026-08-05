# Semana 1 — Primera llamada a Claude API, modelos gratuitos y locales

## Scripts

### Etapa 1 — Primera llamada a la API

| Script | Proveedor | Costo | Descripción |
|--------|-----------|-------|-------------|
| `hello_claude.py` | Claude API (Anthropic) | Pago | Primera llamada a Anthropic, respuesta sobre STM32F407 |
| `hello_mistral.py` | Mistral API (mistral-small) | **Gratis** | Misma pregunta usando un modelo gratuito en la nube |
| `hello_local.py` | LM Studio (local) | **Gratis** | Misma pregunta usando un modelo local vía LM Studio |
| `multi_provider.py` | Claude + Mistral + Local | — | Compara los tres proveedores lado a lado |

### Etapa 2 — Análisis de tokens y costo

| Script | Proveedor | Descripción |
|--------|-----------|-------------|
| `tokens_analisis.py` | Mistral + Claude | Compara consumo de tokens y costo con 256, 512 y 1024 max_tokens |

### Etapa 3 — Experimentos con el prompt

| Script | Proveedor | Descripción |
|--------|-----------|-------------|
| `prompt_experiments.py` | Claude | Sin system prompt vs con system prompt, temperature 0 vs 0.9 |

### Etapa 4 — Múltiples preguntas en loop

| Script | Proveedor | Descripción |
|--------|-----------|-------------|
| `batch_topics.py` | Mistral | 6 temas STM32 en loop, guarda respuestas en `.md` automáticamente |

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

## `hello_mistral.py` — alternativa gratuita en la nube

Mistral ofrece un tier gratuito con `mistral-small-latest` a través de una API compatible con OpenAI.

```
.env (MISTRAL_API_KEY)
    ↓
OpenAI(base_url="https://api.mistral.ai/v1")   ← mismo cliente que LM Studio
    ↓
client.chat.completions.create(model="mistral-small-latest")
    ↓
response.choices[0].message.content
```

**Obtener API key:** https://console.mistral.ai → Sign up → API Keys

---

## `hello_local.py` — alternativa gratuita sin internet

LM Studio expone una API compatible con OpenAI en `http://localhost:1234/v1`. Útil cuando necesitas privacidad total o no tienes conexión.

### Modelos usados en este proyecto

| Modelo | Cuantización | PC | VRAM aprox |
|--------|-------------|-----|-----------|
| Qwen3 9B | Q4_K_M | PC nueva (RTX 5060 8GB) | ~6GB |
| Llama 3.3 8B Instruct | Q5_K_M | PC nueva (RTX 5060 8GB) | ~6GB |
| TinyLlama 1.1B | — | PC antigua (GTX 1050 Ti 4GB) | ~1GB |

```
LM Studio corriendo con modelo cargado
    ↓
OpenAI(base_url="http://localhost:1234/v1")   ← apunta al servidor local
    ↓
client.chat.completions.create()
    ↓
response.choices[0].message.content
```

> Antes de correr este script, asegúrate de tener LM Studio abierto con un modelo cargado y el servidor iniciado.

---

## `multi_provider.py`

Llama a los tres proveedores con la misma pregunta y muestra las respuestas lado a lado.

```
misma pregunta
    ├── ask_claude()   → Claude Haiku   (pago,   API remota)
    ├── ask_mistral()  → Mistral Small  (gratis, API remota)
    └── ask_local()    → LM Studio      (gratis, localhost)
            ↓
    print lado a lado
```

---

## `tokens_analisis.py`

Corre la misma pregunta con `max_tokens` de 256, 512 y 1024 en Mistral y Claude. Imprime una tabla comparativa con tokens consumidos, si la respuesta fue cortada y costo estimado en USD.

```
misma pregunta × 3 valores de max_tokens
    ├── Mistral Small  → tokens + costo
    └── Claude Haiku   → tokens + costo
            ↓
    tabla comparativa en consola
```

---

## `prompt_experiments.py`

Cuatro llamadas a Claude con el mismo tema, variando el prompt y la temperatura:

| Experimento | Qué cambia | Qué observar |
|-------------|------------|--------------|
| EXP 1 | Sin system prompt (baseline) | Respuesta por defecto |
| EXP 2 | System prompt de experto STM32 | ¿Aparece código HAL? |
| EXP 3a | Temperature 0.0 | Respuesta determinista |
| EXP 3b | Temperature 0.9 | Respuesta más creativa |

---

## `batch_topics.py`

Itera sobre 6 temas STM32, pregunta a Mistral sobre cada uno y genera un archivo `.md` con todas las respuestas.

```
TEMAS = [DMA, UART, TIM2 vs TIM6, ADC+DMA, EXTI, SysTick]
    ↓ loop
    llamar_mistral(tema)  → respuesta + tokens
    ↓
respuestas_batch_YYYYMMDD_HHMMSS.md   ← generado automáticamente
    ↓
resumen: tokens totales + costo estimado
```

---

## Mapa de opciones

```
¿Tienes presupuesto para API?
    ├── Sí  → Claude API   (mejor calidad técnica, código HAL)
    └── No  ┬── ¿Tienes internet?
            │    ├── Sí  → Mistral API  (gratis, muy detallado)
            │    └── No  → LM Studio    (gratis, local, sin GPU usa modelos pequeños)
            └── ¿Necesitas privacidad total?
                          → LM Studio   (los datos no salen de tu máquina)
```

---

## Por qué `messages` es una lista

La API es stateless — no recuerda conversaciones anteriores. Cada llamada envía el historial completo. Más adelante (Semana 2) esto importa cuando construyamos cadenas con LangChain.

---

## Cómo correr cada script

```bash
# Windows (PowerShell) — desde la raíz del proyecto
.venv\Scripts\activate

# Etapa 1
python semana01/hello_claude.py          # requiere ANTHROPIC_API_KEY
python semana01/hello_mistral.py         # requiere MISTRAL_API_KEY
python semana01/hello_local.py           # requiere LM Studio abierto con modelo cargado
python semana01/multi_provider.py        # los tres lado a lado

# Etapa 2
python semana01/tokens_analisis.py       # requiere ANTHROPIC_API_KEY + MISTRAL_API_KEY

# Etapa 3
python semana01/prompt_experiments.py    # requiere ANTHROPIC_API_KEY

# Etapa 4
python semana01/batch_topics.py          # requiere MISTRAL_API_KEY

# Linux / macOS — desde la raíz del proyecto
source .venv/bin/activate
python semana01/hello_claude.py
python semana01/hello_mistral.py
python semana01/hello_local.py
python semana01/multi_provider.py
python semana01/tokens_analisis.py
python semana01/prompt_experiments.py
python semana01/batch_topics.py
```

---

## Herramienta adicional: OpenCode

**OpenCode** es una alternativa gratuita y open-source a Claude Code (esta herramienta). Funciona como asistente de código en la terminal y soporta proveedores gratuitos.

- Repositorio: https://github.com/sst/opencode
- Ideal para quienes no quieren pagar por Claude Code pero quieren un asistente de código en terminal.

---

## Qué sigue

En **Semana 2** esto evoluciona a una chain con LangChain:
`prompt template → LLM → output parser → JSON estructurado`
