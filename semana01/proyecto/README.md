# Proyecto Semana 1 — Comparador de modelos

## Objetivo
Verificar que sabes conectarte a múltiples proveedores, medir el costo real y generar un reporte automatizado.

## Qué hace
- Envía la misma pregunta técnica a **Claude** y **Mistral**
- Mide tokens consumidos y calcula el costo en USD por cada proveedor
- Genera un archivo `.md` con las respuestas lado a lado

## Uso

```bash
# Pregunta por defecto (DMA STM32F407)
python semana01/proyecto/comparador_modelos.py

# Pregunta personalizada
python semana01/proyecto/comparador_modelos.py --pregunta "¿Cómo configuro SPI1 en el STM32F407?"
```

## Salida esperada

```
Pregunta: ...
Consultando Claude...
  tokens: 48 in / 512 out  |  $0.000652
Consultando Mistral...
  tokens: 52 in / 489 out  |  $0.000153

Reporte generado: semana01/proyecto/reporte_20260807_143022.md
Costo total estimado: $0.000805 USD
```

## Conceptos que aplica
- Llamadas a múltiples APIs (semana 1)
- Lectura de `response.usage` para tokens
- Generación de archivos automáticamente
- Argparse para CLI simple
