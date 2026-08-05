import os
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

QUESTION = (
    "Soy ingeniero electrónico trabajando con el STM32F407. "
    "Explícame brevemente cómo funciona el DMA controller de este micro "
    "y en qué casos conviene usarlo en lugar de interrupciones."
)

def ask_claude(question: str) -> str:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": question}],
    )
    return message.content[0].text

def ask_local(question: str) -> str:
    client = OpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
    )
    response = client.chat.completions.create(
        model="local-model",
        max_tokens=512,
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content

def ask_mistral(question: str) -> str:
    client = OpenAI(
        base_url="https://api.mistral.ai/v1",
        api_key=os.getenv("MISTRAL_API_KEY"),
    )
    response = client.chat.completions.create(
        model="mistral-small-latest",
        max_tokens=512,
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content

def print_response(provider: str, text: str) -> None:
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"  {provider}")
    print(separator)
    print(text)

if __name__ == "__main__":
    print(f"Pregunta: {QUESTION}\n")

    print_response("CLAUDE Haiku      |  pago   |  Anthropic API", ask_claude(QUESTION))
    print_response("Mistral Small     |  gratis |  Mistral API",   ask_mistral(QUESTION))
    print_response("Modelo local      |  gratis |  LM Studio",     ask_local(QUESTION))
