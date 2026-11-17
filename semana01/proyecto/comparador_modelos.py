"""
Proyecto Semana 1 — Comparador de modelos
==========================================
Hace la misma pregunta técnica a Claude y Mistral,
genera un reporte .md con la comparación lado a lado,
tokens usados y costo estimado por proveedor.

Uso:
    python semana01/proyecto/comparador_modelos.py
    python semana01/proyecto/comparador_modelos.py --pregunta "¿Cómo configuro SPI1?"
"""

import os
import argparse
from datetime import datetime
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PREGUNTA_DEFAULT = (
    "Soy ingeniero electrónico trabajando con el STM32F407. "
    "Explícame cómo funciona el DMA controller y en qué casos "
    "conviene usarlo en lugar de interrupciones."
)

# Costo por millón de tokens (referencia 2026)
COSTOS = {
    "claude": {"input": 0.25, "output": 1.25},
    "mistral": {"input": 0.10, "output": 0.30},
}


def preguntar_claude(pregunta: str) -> dict:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": pregunta}],
    )
    inp = message.usage.input_tokens
    out = message.usage.output_tokens
    costo = inp / 1e6 * COSTOS["claude"]["input"] + out / 1e6 * COSTOS["claude"]["output"]
    return {
        "modelo": "claude-haiku-4-5-20251001",
        "proveedor": "Anthropic API",
        "respuesta": message.content[0].text,
        "input_tokens": inp,
        "output_tokens": out,
        "costo_usd": costo,
        "cortada": message.stop_reason == "max_tokens",
    }


def preguntar_mistral(pregunta: str) -> dict:
    client = OpenAI(
        base_url="https://api.mistral.ai/v1",
        api_key=os.getenv("MISTRAL_API_KEY"),
    )
    response = client.chat.completions.create(
        model="mistral-small-latest",
        max_tokens=1024,
        messages=[{"role": "user", "content": pregunta}],
    )
    inp = response.usage.prompt_tokens
    out = response.usage.completion_tokens
    costo = inp / 1e6 * COSTOS["mistral"]["input"] + out / 1e6 * COSTOS["mistral"]["output"]
    return {
        "modelo": "mistral-small-latest",
        "proveedor": "Mistral API",
        "respuesta": response.choices[0].message.content,
        "input_tokens": inp,
        "output_tokens": out,
        "costo_usd": costo,
        "cortada": out >= 1024,
    }


def generar_reporte(pregunta: str, resultados: list[dict]) -> str:
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = f"semana01/proyecto/reporte_{timestamp}.md"

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(f"# Reporte de comparación de modelos\n\n")
        f.write(f"**Fecha:** {ahora}  \n")
        f.write(f"**Pregunta:** {pregunta}\n\n")
        f.write("---\n\n")

        # Tabla resumen
        f.write("## Resumen\n\n")
        f.write("| Modelo | Proveedor | Input | Output | Costo USD | Cortada |\n")
        f.write("|--------|-----------|-------|--------|-----------|--------|\n")
        for r in resultados:
            cortada = "Sí ⚠" if r["cortada"] else "No ✓"
            f.write(f"| `{r['modelo']}` | {r['proveedor']} | {r['input_tokens']} | {r['output_tokens']} | ${r['costo_usd']:.6f} | {cortada} |\n")
        f.write("\n---\n\n")

        # Respuestas completas
        for r in resultados:
            f.write(f"## {r['proveedor']} — `{r['modelo']}`\n\n")
            f.write(r["respuesta"])
            f.write("\n\n---\n\n")

    return archivo


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comparador de modelos STM32")
    parser.add_argument("--pregunta", type=str, default=PREGUNTA_DEFAULT)
    args = parser.parse_args()

    print(f"Pregunta: {args.pregunta}\n")
    print("Consultando Claude...")
    claude = preguntar_claude(args.pregunta)
    print(f"  tokens: {claude['input_tokens']} in / {claude['output_tokens']} out  |  ${claude['costo_usd']:.6f}")

    print("Consultando Mistral...")
    mistral = preguntar_mistral(args.pregunta)
    print(f"  tokens: {mistral['input_tokens']} in / {mistral['output_tokens']} out  |  ${mistral['costo_usd']:.6f}")

    archivo = generar_reporte(args.pregunta, [claude, mistral])

    print(f"\nReporte generado: {archivo}")
    print(f"Costo total estimado: ${claude['costo_usd'] + mistral['costo_usd']:.6f} USD")
