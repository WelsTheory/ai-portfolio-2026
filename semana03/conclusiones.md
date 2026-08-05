# Semana 3 — Conclusiones

## Qué se probó

| Script | Proveedor | Resultado |
|--------|-----------|-----------|
| `agente_basico.py` | Claude Haiku | OK |
| `agente_mistral.py` | Mistral Small | OK (pausa de 5s entre preguntas por rate limit) |

---

## Observaciones

### `agente_basico.py`
- El agente usó correctamente las tres tools según la pregunta — ninguna llamada fue incorrecta.
- Los cálculos fueron exactos: BRR=0x02D9, PSC=83, frecuencia real=1000Hz.
- Para la pregunta de SPI1 el agente usó `consultar_periferico` en lugar de inventar la respuesta.

### `agente_mistral.py`
- Mismas respuestas correctas que Claude, diferente estilo de presentación.
- Mistral desarrolló más el razonamiento matemático (mostró las fórmulas con LaTeX).
- Sin embargo, en el cálculo del BRR cometió un error conceptual intermedio (`BRR = 0x2D99`) antes de corregirlo — Claude no tuvo ese error.
- Rate limit del tier gratuito requiere pausa de 5s entre preguntas.

### Error de importación resuelto
- En LangChain 1.x / LangGraph 1.0, `create_react_agent` se deprecó en `langgraph.prebuilt`.
- Solución: mantener el import de `langgraph.prebuilt` con `warnings.filterwarnings("ignore")` para suprimir el warning hasta migración oficial.

---

## Diferencia clave vs Semana 2

| | Semana 2 (chain) | Semana 3 (agente) |
|---|---|---|
| Cálculo de BRR | El LLM lo inventa | La tool lo calcula en Python — exacto |
| Flujo | Fijo | El agente decide qué tool usar y cuándo |
| Confianza en el resultado | Hay que verificar | El número viene de código, no del modelo |

---

## Lo que aprendimos

| Concepto | Dónde se ve |
|----------|-------------|
| Agente ReAct con LangGraph | `create_react_agent` en ambos scripts |
| Decorador `@tool` | Las 3 tools STM32 — docstring define cuándo usarlas |
| Tools con cálculo real | `calcular_baudrate`, `calcular_prescaler` — Python calcula, el LLM razona |
| Tools con lookup | `consultar_periferico` — dict como base de datos simple |
| Cambio de proveedor sin tocar tools | `agente_basico.py` vs `agente_mistral.py` — solo cambia el `llm` |
| Error de versión de librería | `create_react_agent` movido entre LangChain y LangGraph en v1.0 |
