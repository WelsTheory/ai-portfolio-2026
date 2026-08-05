import os
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------------
# ETAPA 2 — Análisis de tokens y costo
# Corre la misma pregunta con distintos max_tokens en Mistral y Claude.
# Muestra tokens usados, si la respuesta fue cortada y costo estimado.
# -----------------------------------------------------------------------------

PREGUNTA = (
    "Soy ingeniero electrónico trabajando con el STM32F407. "
    "Explícame brevemente cómo funciona el DMA controller de este micro "
    "y en qué casos conviene usarlo en lugar de interrupciones."
)

# Costo por millón de tokens (referencia agosto 2026)
COSTO_MISTRAL_INPUT  = 0.10   # USD por 1M tokens input  (mistral-small-latest)
COSTO_MISTRAL_OUTPUT = 0.30   # USD por 1M tokens output
COSTO_CLAUDE_INPUT   = 0.25   # USD por 1M tokens input  (claude-haiku-4-5)
COSTO_CLAUDE_OUTPUT  = 1.25   # USD por 1M tokens output

MAX_TOKENS_OPCIONES = [256, 512, 1024]


def llamar_mistral(pregunta: str, max_tokens: int) -> dict:
    client = OpenAI(
        base_url="https://api.mistral.ai/v1",
        api_key=os.getenv("MISTRAL_API_KEY"),
    )
    response = client.chat.completions.create(
        model="mistral-small-latest",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": pregunta}],
    )
    return {
        "texto": response.choices[0].message.content,
        "input":  response.usage.prompt_tokens,
        "output": response.usage.completion_tokens,
        "total":  response.usage.total_tokens,
        "cortada": response.usage.completion_tokens >= max_tokens,
    }


def llamar_claude(pregunta: str, max_tokens: int) -> dict:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": pregunta}],
    )
    input_tokens  = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    return {
        "texto": message.content[0].text,
        "input":  input_tokens,
        "output": output_tokens,
        "total":  input_tokens + output_tokens,
        "cortada": message.stop_reason == "max_tokens",
    }


def calcular_costo(input_tokens: int, output_tokens: int, costo_in: float, costo_out: float) -> float:
    return (input_tokens / 1_000_000 * costo_in) + (output_tokens / 1_000_000 * costo_out)


def imprimir_fila(proveedor: str, max_tokens: int, datos: dict, costo: float) -> None:
    cortada = "Sí ✗" if datos["cortada"] else "No ✓"
    print(f"  {proveedor:<18} {max_tokens:<12} {datos['input']:<10} {datos['output']:<10} {datos['total']:<10} {cortada:<12} ${costo:.6f}")


if __name__ == "__main__":
    print(f"Pregunta: {PREGUNTA}\n")
    print("=" * 90)
    print(f"  {'Proveedor':<18} {'max_tokens':<12} {'Input':<10} {'Output':<10} {'Total':<10} {'Cortada':<12} Costo USD")
    print("=" * 90)

    for max_tok in MAX_TOKENS_OPCIONES:
        datos_mistral = llamar_mistral(PREGUNTA, max_tok)
        costo_mistral = calcular_costo(
            datos_mistral["input"], datos_mistral["output"],
            COSTO_MISTRAL_INPUT, COSTO_MISTRAL_OUTPUT
        )
        imprimir_fila("Mistral Small", max_tok, datos_mistral, costo_mistral)

        datos_claude = llamar_claude(PREGUNTA, max_tok)
        costo_claude = calcular_costo(
            datos_claude["input"], datos_claude["output"],
            COSTO_CLAUDE_INPUT, COSTO_CLAUDE_OUTPUT
        )
        imprimir_fila("Claude Haiku", max_tok, datos_claude, costo_claude)
        print("-" * 90)
