# Proyecto Semana 3 — Asistente de configuración STM32

## Objetivo
Construir un CLI interactivo donde el ingeniero escribe preguntas en lenguaje natural y el agente responde con valores exactos de registros, calculados por tools Python.

## Qué hace
- Loop interactivo en terminal
- El agente decide qué herramienta usar según la pregunta
- Cálculos exactos: BRR para UART, PSC para timers, velocidad SPI
- Lookup de información de periféricos
- Historial de preguntas de la sesión

## Uso

```bash
# Con Claude (pago)
python semana03/proyecto/asistente_stm32.py

# Con Mistral (gratis)
python semana03/proyecto/asistente_stm32.py --mistral
```

## Ejemplo de sesión

```
Tú: ¿Cuál es el BRR para UART1 a 115200 con FCLK 84MHz?
Asistente: El registro BRR debe configurarse con 0x02D9 (mantissa=45, fracción=9)

Tú: ¿Y si quiero 9600 baud?
Asistente: Para 9600 baud el BRR es 0x1B2 (mantissa=27, fracción=2)

Tú: ¿Qué pines usa SPI1?
Asistente: SPI1 usa PA5(SCK), PA6(MISO), PA7(MOSI) en el bus APB2 a 84MHz.

Tú: salir
Sesión terminada. Preguntas realizadas: 3
```

## Tools disponibles

| Tool | Qué calcula |
|------|-------------|
| `calcular_baudrate` | Registro BRR para UART |
| `calcular_prescaler` | PSC para timers |
| `calcular_spi_velocidad` | Velocidad SPI dado el prescaler |
| `consultar_periferico` | Info de pines, bus y velocidad |

## Conceptos que aplica
- Agente ReAct con LangGraph (semana 3)
- Tools con cálculo real en Python
- CLI interactivo con loop
- Mismo agente, dos proveedores (`--mistral`)
