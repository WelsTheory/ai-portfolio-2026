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
            {
                "role": "user", 
                "content": "3 ideas de proyectos de Python para un ingeniero electrónico que trabaja con microcontroladores que pueda usar claude API"
            }
        ],
    )
    for block in message.content:
        if block.type == "text":
            print(block.text, end="")

if __name__ == "__main__":
    main()