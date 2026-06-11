import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# LM Studio expone una API compatible con OpenAI en localhost:1234
# Asegúrate de tener un modelo cargado en LM Studio antes de correr esto
client = OpenAI(
    base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
    api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
)

response = client.chat.completions.create(
    model="local-model",  # LM Studio ignora este valor, usa el modelo que tengas cargado
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
