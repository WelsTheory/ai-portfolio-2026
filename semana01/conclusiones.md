# Semana 1 — Conclusiones

## Qué se probó

### Etapa 1 — Primera llamada a la API

| Script | Proveedor | Costo | Resultado |
|--------|-----------|-------|-----------|
| `hello_claude.py` | Claude Haiku (Anthropic API) | Pago | OK |
| `hello_mistral.py` | Mistral Small (Mistral API) | Gratis | OK |
| `hello_local.py` | Modelo local via LM Studio | Gratis | OK |
| `multi_provider.py` | Los tres lado a lado | — | OK |

### Etapa 2 — Análisis de tokens y costo

| Script | Proveedor | Resultado |
|--------|-----------|-----------|
| `tokens_analisis.py` | Mistral + Claude | Pendiente |

### Etapa 3 — Experimentos con el prompt

| Script | Proveedor | Resultado |
|--------|-----------|-----------|
| `prompt_experiments.py` | Claude | Pendiente |

### Etapa 4 — Múltiples preguntas en loop

| Script | Proveedor | Resultado |
|--------|-----------|-----------|
| `batch_topics.py` | Mistral | Pendiente |

---

## Comparación de respuestas

### Calidad y estructura

| Aspecto | Claude Haiku | Mistral Small | Modelo local |
|---------|-------------|---------------|--------------|
| Estructura | Tablas, secciones, diagrama ASCII | Secciones detalladas con tabla | Prosa con bullets |
| Código HAL | Sí — ejemplo completo con callback | No | No |
| Precisión técnica | Alta | Alta | Media |
| Detalle técnico | General | Registros CR/NDTR/PAR/MAR, modos circular y double buffer | General |
| Contenido extra | Solo respondió lo pedido | Solo respondió lo pedido | Agregó preguntas sin que se le pidieran |

### Errores técnicos detectados

**Modelo local:** afirmó que el STM32F407 tiene **7 canales DMA** — incorrecto.

**Mistral Small:** describió la arquitectura como "16 canales (0-15), cada uno con hasta 8 streams" — la estructura real es la inversa: **2 controladores DMA, cada uno con 8 streams, y cada stream con 8 canales posibles**.

> Referencia correcta: el STM32F407 tiene **2 controladores DMA** (DMA1 y DMA2) con **8 streams cada uno**, para un total de 16 streams independientes.

Mistral fue el más detallado de los tres, pero aun así invirtió la jerarquía canales/streams. **Siempre verificar contra el datasheet oficial.**

---

## Observaciones sobre `max_tokens`

Ambos modelos cortaron la respuesta antes de terminar con `max_tokens=512`. En el caso de Claude Haiku, el ejemplo de código C quedó incompleto (`void DMA_`...).

**Ajuste recomendado para respuestas largas:** usar `max_tokens=1024` o más.

---

## Cuándo usar cada proveedor

| Caso de uso | Recomendación |
|-------------|---------------|
| Documentación técnica precisa con código HAL | Claude API |
| Exploración técnica detallada sin costo | Mistral API |
| Tareas privadas (datos que no deben salir de la máquina) | Modelo local |
| Prototipado rápido sin costo ni internet | Modelo local |
| Comparación de calidad entre modelos | `multi_provider.py` |

---

## Lo que aprendemos en cada etapa

| Etapa | Script | Concepto clave |
|-------|--------|----------------|
| 1 | `hello_*.py` | Cómo conectarse a distintas APIs con el mismo cliente |
| 1 | `multi_provider.py` | Diferencias de calidad entre modelos pago y gratis |
| 2 | `tokens_analisis.py` | Cómo medir consumo y estimar costo de cada llamada |
| 3 | `prompt_experiments.py` | Cómo el system prompt y la temperatura cambian la respuesta |
| 4 | `batch_topics.py` | Cómo automatizar múltiples preguntas y exportar resultados |

---

## Lo que aprendimos sobre la API

- La API es **stateless**: cada llamada envía el historial completo, no recuerda conversaciones anteriores.
- `model`, `max_tokens` y `messages` son los tres parámetros esenciales.
- `messages` es una lista — el mismo mecanismo que se usará en Semana 2 para historial de conversación.
- LM Studio expone una API compatible con OpenAI en `localhost:1234/v1`, lo que permite usar el mismo cliente (`openai`) para cualquier modelo local.

---

## Próximo paso

En **Semana 2** se reemplaza la llamada raw al SDK por una chain con LangChain:

```
Semana 1:  client.messages.create()  →  message.content[0].text
Semana 2:  PromptTemplate | ChatAnthropic | OutputParser  →  str o Pydantic
```
