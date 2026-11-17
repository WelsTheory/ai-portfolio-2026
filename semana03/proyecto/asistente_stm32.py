"""
Proyecto Semana 3 — Asistente de configuración STM32
=====================================================
CLI interactivo donde el ingeniero escribe preguntas
en lenguaje natural y el agente responde con valores
exactos de registros usando herramientas Python.

Uso:
    python semana03/proyecto/asistente_stm32.py
    python semana03/proyecto/asistente_stm32.py --mistral   (versión gratuita)

Comandos en el CLI:
    salir / exit / q    → termina la sesión
    historial           → muestra preguntas de esta sesión
"""

import argparse
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()


# --- Herramientas STM32 ---

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
def calcular_spi_velocidad(fclk_mhz: float, prescaler: int) -> str:
    """Calcula la velocidad de SPI dado el prescaler (BR bits en CR1).
    Parámetros: fclk_mhz (reloj APB en MHz), prescaler (2, 4, 8, 16, 32, 64, 128, 256).
    """
    valores_validos = [2, 4, 8, 16, 32, 64, 128, 256]
    if prescaler not in valores_validos:
        return f"Prescaler inválido. Valores válidos: {valores_validos}"
    velocidad = fclk_mhz / prescaler
    br_bits = valores_validos.index(prescaler)
    return (
        f"SPI con FCLK={fclk_mhz}MHz y prescaler={prescaler}:\n"
        f"  Velocidad : {velocidad:.3f} MHz\n"
        f"  BR[2:0]   : {br_bits:03b} ({br_bits} decimal en CR1)"
    )


@tool
def consultar_periferico(nombre: str) -> str:
    """Devuelve información básica sobre un periférico del STM32F407.
    Parámetros: nombre del periférico (ej: UART1, SPI1, TIM2, ADC1, DMA1, I2C1).
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


tools = [calcular_baudrate, calcular_prescaler, calcular_spi_velocidad, consultar_periferico]

SYSTEM_PROMPT = (
    "Eres un asistente de configuración para microcontroladores STM32F407. "
    "Usa siempre las herramientas disponibles para calcular valores exactos de registros. "
    "Nunca inventes valores numéricos — usa las tools para calcularlos. "
    "Responde en español de forma concisa y técnica."
)

SALIR = {"salir", "exit", "q", "quit"}
AYUDA = {"ayuda", "help", "?"}


def crear_agente(usar_mistral: bool):
    if usar_mistral:
        llm = ChatMistralAI(model="mistral-small-latest", max_tokens=1024)
        print("Modelo: Mistral Small (gratis)\n")
    else:
        llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=1024)
        print("Modelo: Claude Haiku\n")
    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


def main():
    parser = argparse.ArgumentParser(description="Asistente STM32F407")
    parser.add_argument("--mistral", action="store_true", help="Usar Mistral (gratis) en lugar de Claude")
    args = parser.parse_args()

    print("=" * 60)
    print("  Asistente de configuración STM32F407")
    print("  Escribe 'salir' para terminar | 'ayuda' para ejemplos")
    print("=" * 60)

    agent = crear_agente(args.mistral)
    historial_preguntas = []

    while True:
        try:
            pregunta = input("\nTú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSesión terminada.")
            break

        if not pregunta:
            continue

        if pregunta.lower() in SALIR:
            print(f"\nSesión terminada. Preguntas realizadas: {len(historial_preguntas)}")
            break

        if pregunta.lower() in AYUDA:
            print("\nEjemplos de preguntas:")
            print("  ¿Cuál es el BRR para UART1 a 115200 baud con FCLK 84MHz?")
            print("  Necesito un timer a 500Hz con ARR=499 y FCLK 84MHz")
            print("  ¿Qué velocidad tiene SPI1 con prescaler 4 y FCLK 84MHz?")
            print("  ¿Qué pines usa I2C1?")
            continue

        historial_preguntas.append(pregunta)
        resultado = agent.invoke({"messages": [{"role": "user", "content": pregunta}]})
        respuesta = resultado["messages"][-1].content
        print(f"\nAsistente: {respuesta}")


if __name__ == "__main__":
    main()
