import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
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

print(message.content[0].text)
