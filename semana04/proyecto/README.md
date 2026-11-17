# Proyecto Semana 4 — Pipeline de revisión de código STM32

## Objetivo
Construir un pipeline multi-agente con LangGraph que revisa código C de STM32 en tres etapas secuenciales, demostrando cómo coordinar agentes con estado compartido.

## Qué hace
- Recibe código C de STM32 (ejemplo incluido o archivo externo)
- **Agente 1 — Analizador:** describe qué hace el código
- **Agente 2 — Detector:** encuentra errores comunes de HAL/STM32
- **Agente 3 — Mejorador:** sugiere optimizaciones priorizadas
- Genera un reporte `.md` con los tres análisis consolidados

## Uso

```bash
# Con código de ejemplo incluido (UART1 con interrupciones)
python semana04/proyecto/revisor_codigo.py

# Con tu propio archivo .c
python semana04/proyecto/revisor_codigo.py --archivo ruta/a/mi_codigo.c
```

## Flujo del pipeline

```
código C
    ↓
[Agente 1: Analizar]    → descripción de qué hace
    ↓
[Agente 2: Detectar]    → lista de errores con línea y descripción
    ↓
[Agente 3: Mejorar]     → mejoras priorizadas por impacto
    ↓
reporte_revision_YYYYMMDD_HHMMSS.md
```

## Errores que detecta el Agente 2
- Falta de verificación del valor de retorno de funciones HAL
- Buffer overflow en recepciones con DMA
- Callbacks sin validación de instancia (`huart->Instance`)
- Falta de `__HAL_RCC_*_CLK_ENABLE()` antes de inicializar periféricos
- Uso incorrecto de `HAL_UART_Receive_IT` con buffers grandes

## Conceptos que aplica
- LangGraph `StateGraph` con estado compartido (semana 4)
- Pipeline secuencial con `add_edge`
- Cada nodo recibe el resultado del anterior como contexto
- Generación de reporte consolidado multi-agente
