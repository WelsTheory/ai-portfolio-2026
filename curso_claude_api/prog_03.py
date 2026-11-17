from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = "claude-sonnet-5-5"

MAX_HISTORY_MESSAGES = 12

def keep_recent_messages(messages: list[dict[str,str]], max_messages: int = MAX_HISTORY_MESSAGES) -> list[dict]:
    """Conserva solo los ultimos turnos para controlar latencia, contexto y tokens."""
    return messages[-max_messages:]

def summarize_history(client: Anthropic, messages: list[dict[str,str]]) -> str:
    """Resume el historial de mensajes para controlar latencia, contexto y tokens."""
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system="Resume un conversacion para preservar el contexto importante",
        messages=[
            {"role": "user", "content": f"Resume el siguiente historial de mensajes:\n{transcript}"}
        ],
    )
    return "".join(block.text for block in response.content if block.type == "text")

def require_api_key() -> str:
    """Lee la API key de la variable de entorno y lanza un error si no está definida."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY antes de ejecutar este script.")
    return api_key

def main() -> None:
    client = Anthropic(api_key=require_api_key())
    messages=[
        {"role": "user", "content": "Generador de drivers a partir de datasheets"},
        {"role": "assistant", "content": "Claro, Puedo ayudarte a generar drivers a partir de datasheets. Para comenzar, por favor proporciona el datasheet del componente para el cual deseas generar el driver, y especifica el lenguaje de programación y la plataforma de destino (por ejemplo, C para microcontroladores STM32)."},
        {"role": "user", "content": "Recuerdame cual era mi proyecto y sugiere el primer feature"}
    ]
    summary = summarize_history(client, messages)
    controlled_history = []

    for block in message.content:
        if block.type == "text":
            print(block.text, end="")

if __name__ == "__main__":
    main()