import os
from anthropic import Anthropic

MODEL = "claude-sonnet-5-5"

def require_api_key() -> str:
    """Lee la API key de la variable de entorno y lanza un error si no está definida."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY antes de ejecutar este script.")
    return api_key

def main() -> None:
    client = Anthropic(api_key=require_api_key())
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system="Eres un mentor breve y practico de Python",
        messages=[
            {"role": "user", "content": "Generador de drivers a partir de datasheets"},
            {"role": "assistant", "content": "Claro, Puedo ayudarte a generar drivers a partir de datasheets. Para comenzar, por favor proporciona el datasheet del componente para el cual deseas generar el driver, y especifica el lenguaje de programación y la plataforma de destino (por ejemplo, C para microcontroladores STM32)."},
            {"role": "user", "content": "Recuerdame cual era mi proyecto y sugiere el primer feature"}
        ],
    )
    for block in message.content:
        if block.type == "text":
            print(block.text, end="")

if __name__ == "__main__":
    main()