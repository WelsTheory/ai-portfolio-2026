# Proyecto Semana 2 — Generador de documentación HAL

## Objetivo
Demostrar que puedes usar structured output para generar documentación técnica real y útil de forma automática.

## Qué hace
- Recibe una lista de periféricos STM32F407
- Genera documentación completa para cada uno usando `with_structured_output()` + Pydantic
- Exporta todo en un único archivo `.md` listo para usar

## Uso

```bash
# Periféricos por defecto (UART1, SPI1, TIM2, ADC1, DMA2)
python semana02/proyecto/generador_docs.py

# Periféricos específicos
python semana02/proyecto/generador_docs.py --perifericos UART1 I2C1 TIM6
```

## Salida esperada

```
Generando documentación para: UART1, SPI1, TIM2, ADC1, DMA2

  [UART1] consultando...
  [UART1] OK
  [SPI1] consultando...
  ...

Documentación generada: semana02/proyecto/docs_hal_20260807_143022.md
```

El `.md` generado contiene por cada periférico:
- Descripción y bus
- Registros clave
- Código HAL de ejemplo
- Cuándo usar DMA vs interrupciones
- Nota de configuración

## Conceptos que aplica
- LCEL chain con structured output (semana 2)
- Pydantic como schema de salida
- Generación de documentación automatizada
- Argparse para CLI
