import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Mistral expone una API compatible con OpenAI — misma interfaz, distinto base_url
# Modelo usado: mistral-small-latest — disponible en el tier gratuito
# API key en: https://console.mistral.ai

client = OpenAI(
    base_url="https://api.mistral.ai/v1",
    api_key=os.getenv("MISTRAL_API_KEY"),
)

response = client.chat.completions.create(
    model="mistral-small-latest",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": (
                "Soy ingeniero electrónico trabajando con el STM32F407. "
                "Explícame brevemente cómo funciona el DMA controller de este micro "
                "y en qué casos conviene usarlo en lugar de interrupciones."
            ),
        }
    ],
)

print(response.choices[0].message.content)

# -----------------------------------------------------------------------------
# ETAPA 2 — Ver consumo de tokens
# Descomentar cuando quieras analizar cuántos tokens usa cada llamada
# -----------------------------------------------------------------------------
# print(f"\n--- Tokens usados ---")
# print(f"Input : {response.usage.prompt_tokens}")
# print(f"Output: {response.usage.completion_tokens}")
# print(f"Total : {response.usage.total_tokens}")
