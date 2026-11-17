"""
Proyecto Semana 4 — Pipeline de revisión de código STM32
=========================================================
Multi-agente con LangGraph que recibe código C de STM32,
lo analiza en tres etapas independientes y genera un
reporte consolidado.

Agentes:
  1. Analizador  → entiende qué hace el código
  2. Detector    → encuentra errores comunes de STM32/HAL
  3. Mejorador   → sugiere optimizaciones y buenas prácticas

Uso:
    python semana04/proyecto/revisor_codigo.py
    python semana04/proyecto/revisor_codigo.py --archivo mi_codigo.c
"""

import argparse
from datetime import datetime
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from typing import TypedDict

load_dotenv()

# --- Código de ejemplo para demostración ---
CODIGO_EJEMPLO = """
#include "stm32f4xx_hal.h"

UART_HandleTypeDef huart1;
uint8_t rx_buffer[256];

void UART_Init(void) {
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    HAL_UART_Init(&huart1);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    // Procesar dato recibido
    HAL_UART_Receive_IT(&huart1, rx_buffer, 1);
}

int main(void) {
    HAL_Init();
    UART_Init();
    HAL_UART_Receive_IT(&huart1, rx_buffer, 256);

    while(1) {
        HAL_Delay(100);
    }
}
"""


# --- Estado del grafo ---
class EstadoRevision(TypedDict):
    codigo: str
    analisis: str
    errores: str
    mejoras: str


# --- Modelo ---
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=1024)
parser = StrOutputParser()


# --- Nodos del grafo ---

def nodo_analizar(estado: EstadoRevision) -> dict:
    """Agente 1: entiende qué hace el código."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un experto en STM32F407. Analiza el código C proporcionado."),
        ("human", "Describe qué hace este código de forma concisa y técnica:\n\n```c\n{codigo}\n```"),
    ])
    chain = prompt | llm | parser
    resultado = chain.invoke({"codigo": estado["codigo"]})
    print("  [1/3] Análisis completado")
    return {"analisis": resultado}


def nodo_detectar_errores(estado: EstadoRevision) -> dict:
    """Agente 2: encuentra errores comunes de STM32/HAL."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Eres un experto en STM32F407 y HAL. "
            "Detecta errores comunes como: falta de verificación de retorno HAL, "
            "buffer overflow, callbacks sin validación de instancia, "
            "uso incorrecto de DMA, falta de __HAL_RCC_*_CLK_ENABLE."
        )),
        ("human", (
            "Encuentra errores en este código. "
            "Contexto: {analisis}\n\n"
            "Código:\n```c\n{codigo}\n```\n\n"
            "Lista cada error con: línea aproximada, descripción y por qué es un problema."
        )),
    ])
    chain = prompt | llm | parser
    resultado = chain.invoke({"codigo": estado["codigo"], "analisis": estado["analisis"]})
    print("  [2/3] Detección de errores completada")
    return {"errores": resultado}


def nodo_mejorar(estado: EstadoRevision) -> dict:
    """Agente 3: sugiere optimizaciones y buenas prácticas."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Eres un experto en firmware STM32F407. "
            "Sugiere mejoras concretas: uso de DMA donde convenga, "
            "manejo de errores HAL, optimización de buffers, "
            "buenas prácticas de naming y estructura."
        )),
        ("human", (
            "Sugiere mejoras para este código.\n"
            "Análisis previo: {analisis}\n"
            "Errores detectados: {errores}\n\n"
            "Código:\n```c\n{codigo}\n```\n\n"
            "Proporciona mejoras priorizadas de mayor a menor impacto."
        )),
    ])
    chain = prompt | llm | parser
    resultado = chain.invoke({
        "codigo": estado["codigo"],
        "analisis": estado["analisis"],
        "errores": estado["errores"],
    })
    print("  [3/3] Sugerencias de mejora completadas")
    return {"mejoras": resultado}


# --- Grafo LangGraph ---
def construir_grafo():
    grafo = StateGraph(EstadoRevision)
    grafo.add_node("analizar", nodo_analizar)
    grafo.add_node("detectar_errores", nodo_detectar_errores)
    grafo.add_node("mejorar", nodo_mejorar)

    grafo.set_entry_point("analizar")
    grafo.add_edge("analizar", "detectar_errores")
    grafo.add_edge("detectar_errores", "mejorar")
    grafo.add_edge("mejorar", END)

    return grafo.compile()


def generar_reporte(estado: EstadoRevision, codigo_fuente: str) -> str:
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = f"semana04/proyecto/reporte_revision_{timestamp}.md"

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("# Reporte de revisión de código STM32\n\n")
        f.write(f"**Fecha:** {ahora}\n\n---\n\n")
        f.write("## Código revisado\n\n")
        f.write(f"```c\n{codigo_fuente}\n```\n\n---\n\n")
        f.write("## 1. Análisis\n\n")
        f.write(estado["analisis"])
        f.write("\n\n---\n\n## 2. Errores detectados\n\n")
        f.write(estado["errores"])
        f.write("\n\n---\n\n## 3. Mejoras sugeridas\n\n")
        f.write(estado["mejoras"])
        f.write("\n")

    return archivo


if __name__ == "__main__":
    parser_args = argparse.ArgumentParser(description="Revisor de código STM32")
    parser_args.add_argument("--archivo", type=str, help="Archivo .c a revisar (opcional)")
    args = parser_args.parse_args()

    if args.archivo:
        with open(args.archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    else:
        codigo = CODIGO_EJEMPLO
        print("Usando código de ejemplo (UART1 con interrupciones)\n")

    print("Iniciando revisión con pipeline multi-agente...\n")

    pipeline = construir_grafo()
    estado_inicial = EstadoRevision(codigo=codigo, analisis="", errores="", mejoras="")
    resultado = pipeline.invoke(estado_inicial)

    archivo = generar_reporte(resultado, codigo)
    print(f"\nReporte generado: {archivo}")
