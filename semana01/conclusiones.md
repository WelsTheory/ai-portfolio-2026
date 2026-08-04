# Semana 1 — Conclusiones

## Qué se probó

Se ejecutaron los tres scripts de semana 1 con la misma pregunta técnica sobre el DMA controller del STM32F407:

| Script | Proveedor | Resultado |
|--------|-----------|-----------|
| `hello_claude.py` | Claude Haiku (API remota) | OK |
| `hello_local.py` | Modelo local via LM Studio | OK |
| `multi_provider.py` | Ambos lado a lado | OK |

---

## Comparación de respuestas

### Calidad y estructura

| Aspecto | Claude Haiku | Modelo local |
|---------|-------------|--------------|
| Estructura | Tablas, secciones, diagrama ASCII | Prosa con bullets |
| Código HAL | Sí — ejemplo completo con callback | No |
| Precisión técnica | Alta | Media |
| Contenido extra | Solo respondió lo pedido | Agregó preguntas sin que se le pidieran |

### Error técnico detectado en el modelo local

El modelo local afirmó que el STM32F407 tiene **7 canales DMA**. Esto es incorrecto:

> El STM32F407 tiene **2 controladores DMA** (DMA1 y DMA2) con **8 streams cada uno**, para un total de 16 streams independientes.

Esto confirma una limitación real de los modelos más pequeños en dominios técnicos específicos: generan texto plausible pero no necesariamente exacto. **Siempre verificar contra el datasheet oficial.**

---

## Observaciones sobre `max_tokens`

Ambos modelos cortaron la respuesta antes de terminar con `max_tokens=512`. En el caso de Claude Haiku, el ejemplo de código C quedó incompleto (`void DMA_`...).

**Ajuste recomendado para respuestas largas:** usar `max_tokens=1024` o más.

---

## Cuándo usar cada proveedor

| Caso de uso | Recomendación |
|-------------|---------------|
| Documentación técnica precisa | Claude API |
| Explicaciones con código HAL | Claude API |
| Tareas simples o privadas (sin enviar datos sensibles a la nube) | Modelo local |
| Prototipado rápido sin costo por token | Modelo local |
| Comparación de calidad entre modelos | `multi_provider.py` |

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
