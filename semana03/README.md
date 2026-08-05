# Semana 3 — Agentes + ReAct

## Scripts

| Script | Proveedor | Costo | Descripción |
|--------|-----------|-------|-------------|
| `agente_basico.py` | Claude Haiku | Pago | Agente ReAct con 3 herramientas STM32 |
| `agente_mistral.py` | Mistral Small | **Gratis** | Mismo agente con Mistral |

---

## Diferencia con Semana 2

| | Semana 2 (chain) | Semana 3 (agente) |
|---|---|---|
| **Flujo** | Fijo — siempre prompt → llm → parser | Dinámico — el LLM decide los pasos |
| **Tools** | No | Sí — funciones Python que el agente puede llamar |
| **Iteraciones** | Una sola pasada | Múltiples hasta llegar a la respuesta |
| **Razonamiento** | Ninguno visible | Pensamiento → Acción → Observación (ReAct) |

---

## Herramientas disponibles

| Tool | Qué hace | Ejemplo de uso |
|------|----------|----------------|
| `calcular_baudrate` | Calcula el registro BRR para UART | `fclk_mhz=84, baudrate=115200` |
| `calcular_prescaler` | Calcula PSC para timers | `fclk_mhz=84, frecuencia_hz=1000, arr=999` |
| `consultar_periferico` | Info de periféricos STM32F407 | `nombre="UART1"` |

---

## Ciclo ReAct

```
Pregunta: ¿Cuál es el BRR para UART1 a 115200 baud con FCLK=84MHz?

Pensamiento: Necesito usar calcular_baudrate con fclk_mhz=84 y baudrate=115200
Acción:      calcular_baudrate
Entrada:     {"fclk_mhz": 84, "baudrate": 115200}
Observación: BRR = 0x1D4 (45.3125 → mantissa=45, fracción=5)

Pensamiento: Ya tengo el resultado.
Respuesta:   El registro BRR debe configurarse con el valor 0x1D4.
```

Con `verbose=True` en el `AgentExecutor` puedes ver este razonamiento en consola en tiempo real.

---

## Por qué las tools son funciones Python normales

```python
@tool
def calcular_baudrate(fclk_mhz: float, baudrate: int) -> str:
    """Calcula el valor del registro BRR para configurar UART en STM32."""
    brr = fclk_mhz * 1_000_000 / (16 * baudrate)
    ...
```

El decorador `@tool` hace tres cosas:
1. Expone la función al agente
2. Usa el **docstring** para que el agente sepa cuándo llamarla
3. Convierte los tipos de retorno a string automáticamente

El docstring es crítico — es lo que lee el agente para decidir si usar la tool.

---

## Cómo correr

```bash
# Windows (PowerShell)
.venv\Scripts\activate
python semana03/agente_basico.py      # requiere ANTHROPIC_API_KEY
python semana03/agente_mistral.py     # requiere MISTRAL_API_KEY

# Linux / macOS
source .venv/bin/activate
python semana03/agente_basico.py
python semana03/agente_mistral.py
```

---

## Qué sigue

En **Semana 4** los agentes se coordinan entre sí con LangGraph:
`AgentExecutor → LangGraph → múltiples agentes con estado compartido`
