import time
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from langgraph.prebuilt import create_react_agent

load_dotenv()

# -----------------------------------------------------------------------------
# Semana 3 — Agente ReAct con Mistral (versión gratuita)
# Mismo agente que agente_basico.py, solo cambia el modelo.
# Nota: Mistral tiene rate limit en el tier gratuito.
#       Se agrega pausa entre preguntas para evitar error 429.
# -----------------------------------------------------------------------------


# --- 1. Herramientas (idénticas a agente_basico.py) ---

@tool
def calcular_baudrate(fclk_mhz: float, baudrate: int) -> str:
    """Calcula el valor del registro BRR para configurar UART en STM32.
    Parámetros: fclk_mhz (frecuencia del reloj en MHz), baudrate (ej: 9600, 115200).
    """
    brr = fclk_mhz * 1_000_000 / (16 * baudrate)
    mantissa = int(brr)
    fraction = round((brr - mantissa) * 16)
    hex_val = (mantissa << 4) | fraction
    return (
        f"BRR para {baudrate} baud con FCLK={fclk_mhz}MHz:\n"
        f"  Mantissa : {mantissa}\n"
        f"  Fracción : {fraction}\n"
        f"  Registro : 0x{hex_val:04X}  ({hex_val} decimal)"
    )


@tool
def calcular_prescaler(fclk_mhz: float, frecuencia_hz: float, arr: int) -> str:
    """Calcula el prescaler (PSC) de un timer STM32 para lograr una frecuencia deseada.
    Parámetros: fclk_mhz (reloj en MHz), frecuencia_hz (frecuencia deseada en Hz), arr (valor ARR del timer).
    Fórmula: PSC = (FCLK / (frecuencia * (ARR + 1))) - 1
    """
    psc = (fclk_mhz * 1_000_000 / (frecuencia_hz * (arr + 1))) - 1
    if psc < 0 or psc > 65535:
        return f"PSC={psc:.1f} fuera de rango (0-65535). Ajusta ARR o frecuencia."
    return (
        f"Timer para {frecuencia_hz}Hz con FCLK={fclk_mhz}MHz y ARR={arr}:\n"
        f"  PSC = {int(psc)}\n"
        f"  Frecuencia real = {fclk_mhz * 1_000_000 / ((int(psc) + 1) * (arr + 1)):.2f} Hz"
    )


@tool
def consultar_periferico(nombre: str) -> str:
    """Devuelve información básica sobre un periférico del STM32F407.
    Parámetros: nombre del periférico (ej: UART1, SPI1, TIM2, ADC1, DMA1).
    """
    PERIFERICOS = {
        "UART1":  "Bus APB2 (84MHz). Pines: PA9(TX), PA10(RX). Soporta DMA2.",
        "UART2":  "Bus APB1 (42MHz). Pines: PA2(TX), PA3(RX). Soporta DMA1.",
        "UART3":  "Bus APB1 (42MHz). Pines: PB10(TX), PB11(RX). Soporta DMA1.",
        "SPI1":   "Bus APB2 (84MHz). Pines: PA5(SCK), PA6(MISO), PA7(MOSI). Hasta 42Mbps.",
        "SPI2":   "Bus APB1 (42MHz). Pines: PB13(SCK), PB14(MISO), PB15(MOSI). Hasta 21Mbps.",
        "TIM2":   "Timer 32 bits. Bus APB1. 4 canales PWM/captura. Encoder. Trigger ADC/DAC.",
        "TIM6":   "Timer básico 16 bits. Bus APB1. Sin canales PWM. Solo interrupciones y trigger DAC.",
        "ADC1":   "12 bits, 16 canales. Bus APB2. Modos: single, continuous, scan. Soporta DMA2.",
        "DMA1":   "8 canales. Periféricos: UART2/3, SPI2, I2C1/2, TIM2/3/4/5, DAC.",
        "DMA2":   "8 canales. Periféricos: UART1, SPI1/3, ADC1, SDIO, Ethernet. Alta velocidad.",
        "I2C1":   "Bus APB1. Pines: PB6(SCL), PB7(SDA). Hasta 400kHz (Fast Mode).",
    }
    nombre_upper = nombre.upper()
    if nombre_upper in PERIFERICOS:
        return f"{nombre_upper}: {PERIFERICOS[nombre_upper]}"
    disponibles = ", ".join(PERIFERICOS.keys())
    return f"Periférico '{nombre}' no encontrado. Disponibles: {disponibles}"


tools = [calcular_baudrate, calcular_prescaler, consultar_periferico]


# --- 2. Modelo (Mistral — gratuito) ---
llm = ChatMistralAI(model="mistral-small-latest", max_tokens=1024)


# --- 3. Agente (LangGraph prebuilt ReAct) ---
SYSTEM_PROMPT = (
    "Eres un experto en microcontroladores STM32F407. "
    "Usa las herramientas disponibles para responder con precisión. "
    "Cuando hagas cálculos, muestra los valores intermedios."
)

agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


# --- 4. Preguntas de prueba ---
PREGUNTAS = [
    "¿Cuál es el BRR para configurar UART1 a 115200 baud con FCLK de 84MHz?",
    "Necesito un timer a 1kHz con ARR=999 y FCLK de 84MHz. ¿Qué prescaler uso?",
    "¿Qué bus usa SPI1 y a qué velocidad máxima puede funcionar?",
]

if __name__ == "__main__":
    for i, pregunta in enumerate(PREGUNTAS):
        print(f"\n{'=' * 60}")
        print(f"  PREGUNTA: {pregunta}")
        print("=" * 60)
        resultado = agent.invoke({"messages": [{"role": "user", "content": pregunta}]})
        respuesta_final = resultado["messages"][-1].content
        print(f"\n  RESPUESTA FINAL: {respuesta_final}")
        if i < len(PREGUNTAS) - 1:
            time.sleep(5)   # pausa por rate limit del tier gratuito
