"""
Proyecto Semana 2 — Generador de documentación HAL
===================================================
Dado un periférico STM32F407, genera automáticamente
un archivo .md con documentación completa:
  - Descripción y bus
  - Registros clave
  - Código HAL de ejemplo
  - DMA vs interrupciones
  - Notas de configuración

Uso:
    python semana02/proyecto/generador_docs.py
    python semana02/proyecto/generador_docs.py --perifericos UART1 SPI1 ADC1
"""

import argparse
from datetime import datetime
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

PERIFERICOS_DEFAULT = ["UART1", "SPI1", "TIM2", "ADC1", "DMA2"]


# --- Esquema de documentación ---
class DocPeriferico(BaseModel):
    nombre: str = Field(description="Nombre del periférico, ej: UART1")
    descripcion: str = Field(description="Qué hace este periférico — una oración técnica")
    bus: str = Field(description="Bus al que está conectado (APB1/APB2) y su frecuencia en el STM32F407")
    registros_clave: list[str] = Field(description="Lista de 3-5 registros importantes con su función, ej: 'BRR — Baud Rate Register'")
    codigo_hal: str = Field(description="Ejemplo de código C con HAL para inicializar o usar el periférico")
    cuando_dma: list[str] = Field(description="Lista de casos donde conviene usar DMA con este periférico")
    cuando_interrupcion: list[str] = Field(description="Lista de casos donde conviene usar interrupciones")
    notas: str = Field(description="Una nota importante o advertencia de configuración")


# --- Chain ---
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=2048)
llm_structured = llm.with_structured_output(DocPeriferico)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un experto en microcontroladores STM32F407. "
        "Genera documentación técnica precisa para el periférico indicado. "
        "El código HAL debe ser compilable y representativo.",
    ),
    ("human", "Genera la documentación completa para el periférico: {periferico}"),
])

chain = prompt | llm_structured


def generar_md(doc: DocPeriferico) -> str:
    lineas = [
        f"## {doc.nombre}\n",
        f"**Descripción:** {doc.descripcion}  ",
        f"**Bus:** {doc.bus}\n",
        "### Registros clave\n",
    ]
    for reg in doc.registros_clave:
        lineas.append(f"- {reg}")
    lineas.append("\n### Ejemplo HAL\n")
    lineas.append(f"```c\n{doc.codigo_hal}\n```\n")
    lineas.append("### DMA vs Interrupciones\n")
    lineas.append("**Usar DMA cuando:**")
    for caso in doc.cuando_dma:
        lineas.append(f"- {caso}")
    lineas.append("\n**Usar interrupciones cuando:**")
    for caso in doc.cuando_interrupcion:
        lineas.append(f"- {caso}")
    lineas.append(f"\n> **Nota:** {doc.notas}\n")
    lineas.append("---\n")
    return "\n".join(lineas)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de documentación HAL para STM32F407")
    parser.add_argument("--perifericos", nargs="+", default=PERIFERICOS_DEFAULT)
    args = parser.parse_args()

    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = f"semana02/proyecto/docs_hal_{timestamp}.md"

    contenido = [
        f"# Documentación HAL — STM32F407\n",
        f"Generado: {ahora}  \n",
        f"Periféricos: {', '.join(args.perifericos)}\n\n",
        "---\n\n",
    ]

    print(f"Generando documentación para: {', '.join(args.perifericos)}\n")

    for periferico in args.perifericos:
        print(f"  [{periferico}] consultando...")
        doc = chain.invoke({"periferico": periferico})
        contenido.append(generar_md(doc))
        print(f"  [{periferico}] OK")

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))

    print(f"\nDocumentación generada: {archivo}")
