import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -----------------------------------------------------------------------------
# ETAPA 4 — Múltiples preguntas en loop
# Itera sobre temas STM32, pregunta a Mistral sobre cada uno,
# muestra tokens por pregunta y guarda todo en un archivo .md automáticamente.
# Proveedor: Mistral — varias llamadas seguidas sin gastar créditos de pago
# -----------------------------------------------------------------------------

TEMAS = [
    "¿Cómo funciona el DMA controller del STM32F407 y cuándo usarlo?",
    "¿Cómo configurar UART1 en modo recepción con HAL_UART_Receive_IT?",
    "¿Cuál es la diferencia entre TIM2 y TIM6 en el STM32F407?",
    "¿Cómo usar el ADC1 del STM32F407 con DMA para leer múltiples canales?",
    "¿Cómo configurar una interrupción externa EXTI en el STM32F407?",
    "¿Qué es el SysTick y cómo lo usa HAL_Delay internamente?",
]

ARCHIVO_SALIDA = f"semana01/respuestas_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"


def llamar_mistral(pregunta: str, client: OpenAI) -> dict:
    response = client.chat.completions.create(
        model="mistral-small-latest",
        max_tokens=512,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un experto en microcontroladores STM32. "
                    "Responde de forma técnica y concisa."
                ),
            },
            {"role": "user", "content": pregunta},
        ],
    )
    return {
        "texto":   response.choices[0].message.content,
        "input":   response.usage.prompt_tokens,
        "output":  response.usage.completion_tokens,
        "total":   response.usage.total_tokens,
        "cortada": response.usage.completion_tokens >= 512,
    }


if __name__ == "__main__":
    client = OpenAI(
        base_url="https://api.mistral.ai/v1",
        api_key=os.getenv("MISTRAL_API_KEY"),
    )

    resultados = []
    tokens_totales = 0

    print(f"Procesando {len(TEMAS)} temas...\n")

    for i, tema in enumerate(TEMAS, start=1):
        print(f"[{i}/{len(TEMAS)}] {tema[:60]}...")
        datos = llamar_mistral(tema, client)
        tokens_totales += datos["total"]
        cortada = " ⚠ respuesta cortada" if datos["cortada"] else ""
        print(f"        Tokens: input={datos['input']} output={datos['output']}{cortada}\n")
        resultados.append({"tema": tema, **datos})

    # ------------------------------------------------------------------
    # Guardar en markdown
    # ------------------------------------------------------------------
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write(f"# Respuestas batch — STM32F407\n")
        f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"Modelo: mistral-small-latest  \n")
        f.write(f"Tokens totales: {tokens_totales}\n\n")
        f.write("---\n\n")

        for i, r in enumerate(resultados, start=1):
            f.write(f"## {i}. {r['tema']}\n\n")
            f.write(r["texto"])
            f.write(f"\n\n> Tokens — input: {r['input']} | output: {r['output']} | total: {r['total']}\n\n")
            f.write("---\n\n")

    # ------------------------------------------------------------------
    # Resumen final en consola
    # ------------------------------------------------------------------
    print("=" * 50)
    print(f"  Temas procesados : {len(TEMAS)}")
    print(f"  Tokens totales   : {tokens_totales}")
    print(f"  Costo estimado   : ${tokens_totales / 1_000_000 * 0.30:.6f} USD")
    print(f"  Archivo generado : {ARCHIVO_SALIDA}")
    print("=" * 50)
