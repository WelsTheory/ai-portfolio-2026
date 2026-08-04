from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()


# --- 1. Esquema de salida con Pydantic ---
class AnalisisPeriferico(BaseModel):
    nombre: str = Field(description="Nombre del periférico STM32")
    descripcion: str = Field(description="Qué hace este periférico en una oración")
    casos_dma: list[str] = Field(description="Lista de casos donde conviene usar DMA con este periférico")
    casos_interrupcion: list[str] = Field(description="Lista de casos donde conviene usar interrupciones")
    funcion_hal_ejemplo: str = Field(description="Una función HAL representativa, ej: HAL_UART_Receive_DMA()")
    nivel_complejidad: str = Field(description="Baja | Media | Alta — complejidad de configuración")


# --- 2. Modelo con structured output ---
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=1024)
llm_structured = llm.with_structured_output(AnalisisPeriferico)

# --- 3. Prompt ---
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un experto en microcontroladores STM32F407. "
        "Analiza el periférico indicado y devuelve la información en el formato solicitado.",
    ),
    ("human", "Analiza el periférico: {periferico}"),
])

# --- 4. Chain ---
chain = prompt | llm_structured


# --- 5. Helper para imprimir el resultado ---
def imprimir_analisis(analisis: AnalisisPeriferico) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {analisis.nombre}  |  Complejidad: {analisis.nivel_complejidad}")
    print("=" * 60)
    print(f"Descripción : {analisis.descripcion}")
    print(f"HAL ejemplo : {analisis.funcion_hal_ejemplo}")
    print("\nUsar DMA cuando:")
    for caso in analisis.casos_dma:
        print(f"  • {caso}")
    print("\nUsar interrupciones cuando:")
    for caso in analisis.casos_interrupcion:
        print(f"  • {caso}")


PERIFERICOS = ["UART1", "ADC1", "SPI1"]

if __name__ == "__main__":
    for periferico in PERIFERICOS:
        resultado = chain.invoke({"periferico": periferico})
        imprimir_analisis(resultado)
