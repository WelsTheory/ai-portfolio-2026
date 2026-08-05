import anthropic
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------------
# ETAPA 3 — Experimentos con el prompt
# Mismo tema, tres experimentos:
#   1. Sin system prompt
#   2. Con system prompt de experto STM32
#   3. Temperature 0 (determinista) vs 0.9 (creativo)
# Proveedor: Claude Haiku — resultados más consistentes para ver el efecto del prompt
# -----------------------------------------------------------------------------

TEMA = (
    "Explícame brevemente cómo funciona el DMA controller del STM32F407 "
    "y en qué casos conviene usarlo en lugar de interrupciones."
)


def llamar_claude(messages: list, temperature: float = 1.0, max_tokens: int = 512) -> str:
    client = anthropic.Anthropic()
    kwargs = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": max_tokens,
        "messages": messages,
    }
    # temperature solo se incluye si es distinto al default (la API acepta 0.0–1.0)
    if temperature != 1.0:
        kwargs["temperature"] = temperature

    message = client.messages.create(**kwargs)
    return message.content[0].text


def separador(titulo: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print("=" * 60)


if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Experimento 1 — Sin system prompt (baseline)
    # ------------------------------------------------------------------
    separador("EXP 1 — Sin system prompt (baseline)")
    respuesta_1 = llamar_claude(
        messages=[{"role": "user", "content": TEMA}]
    )
    print(respuesta_1)

    # ------------------------------------------------------------------
    # Experimento 2 — Con system prompt de experto STM32
    # ------------------------------------------------------------------
    separador("EXP 2 — Con system prompt de experto STM32")
    respuesta_2 = llamar_claude(
        messages=[{"role": "user", "content": TEMA}],
    )
    # Nota: anthropic usa el parámetro "system" separado de messages
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=(
            "Eres un ingeniero de firmware senior especializado en STM32. "
            "Responde siempre con ejemplos de código HAL en C. "
            "Sé directo y técnico — el usuario ya conoce electrónica."
        ),
        messages=[{"role": "user", "content": TEMA}],
    )
    respuesta_2 = message.content[0].text
    print(respuesta_2)

    # ------------------------------------------------------------------
    # Experimento 3 — Temperature: 0 (determinista) vs 0.9 (creativo)
    # ------------------------------------------------------------------
    separador("EXP 3a — Temperature 0.0 (determinista)")
    respuesta_3a = llamar_claude(
        messages=[{"role": "user", "content": TEMA}],
        temperature=0.0,
    )
    print(respuesta_3a)

    separador("EXP 3b — Temperature 0.9 (creativo)")
    respuesta_3b = llamar_claude(
        messages=[{"role": "user", "content": TEMA}],
        temperature=0.9,
    )
    print(respuesta_3b)

    # ------------------------------------------------------------------
    # Resumen
    # ------------------------------------------------------------------
    print(f"\n{'=' * 60}")
    print("  RESUMEN — Qué cambió entre experimentos")
    print("=" * 60)
    print("EXP 1 vs EXP 2 : observa si aparece código HAL con system prompt")
    print("EXP 3a vs 3b   : observa si cambia el estilo/estructura de la respuesta")
