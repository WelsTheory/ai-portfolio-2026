# Semana 2 — Conclusiones

## Qué se probó

| Script | Proveedor | Resultado |
|--------|-----------|-----------|
| `chain_basica.py` | Claude Haiku | OK |
| `chain_mistral.py` | Mistral Small | OK (requiere pausa de 3s entre llamadas por rate limit) |
| `chain_json.py` | Claude Haiku | OK |
| `chain_historial.py` | Claude Haiku | OK |

---

## Observaciones

### `chain_basica.py`
- El system prompt de experto STM32 mejoró notablemente la respuesta respecto a semana 1 — el modelo incluyó código HAL completo y tablas comparativas sin pedirlo explícitamente.
- La respuesta sobre ADC+DMA se cortó (`HAL_`) por el límite de `max_tokens=512`.

### `chain_mistral.py`
- El tier gratuito de Mistral tiene rate limit — 3 llamadas seguidas generan error `429`.
- Solución: pausa de 3 segundos entre llamadas con `time.sleep(3)`.
- Mismo chain que `chain_basica.py`, solo cambió `ChatAnthropic` por `ChatMistralAI` — demuestra la portabilidad de LangChain.

### `chain_json.py`
- El modelo devuelve un objeto Pydantic con campos tipados (`nombre`, `casos_dma`, `casos_interrupcion`, `funcion_hal_ejemplo`, `nivel_complejidad`) en lugar de texto libre.
- Los campos son accesibles directamente en código: `resultado.nivel_complejidad`, `resultado.casos_dma`, etc.
- Equivalente a un `struct` en C — el modelo debe rellenar exactamente esos campos.

### `chain_historial.py`
- Conversación de 4 turnos sobre DMA del STM32F407. El modelo respondió correctamente preguntas de seguimiento sin repetir el contexto (`"¿cuántos streams tiene?"` sin mencionar DMA).
- El historial acumuló 9 mensajes: 1 system + 4 pares (HumanMessage + AIMessage).
- Observación técnica importante: Claude corrigió el término "streams" — el STM32F407 usa **canales**, no streams (esa nomenclatura es del STM32F429). Demuestra que con historial el modelo puede hacer correcciones contextuales.
- El costo en tokens crece con cada turno porque cada llamada incluye todos los mensajes anteriores.

---

## Lo que aprendimos

| Concepto | Dónde se ve |
|----------|-------------|
| LCEL pipe `\|` | `chain = prompt \| llm \| parser` |
| PromptTemplate con variables | `{topic}` en `chain_basica.py` |
| Cambiar modelo sin tocar el chain | `chain_basica.py` vs `chain_mistral.py` |
| Rate limit en tier gratuito | Error 429 en `chain_mistral.py` |
| Structured output = struct de C | `chain_json.py` — objeto Pydantic con campos tipados |
| API stateless con historial manual | `chain_historial.py` — historial crece con cada turno |
| El modelo puede corregir errores contextuales | Turno 2 de `chain_historial.py` — corrigió streams vs canales |
