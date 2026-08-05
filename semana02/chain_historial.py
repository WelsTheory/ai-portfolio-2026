from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# -----------------------------------------------------------------------------
# Conversación con historial
# Muestra cómo mantener contexto entre turnos enviando el historial completo.
# Conecta con el concepto de semana 1: la API es stateless, pero si enviamos
# los mensajes anteriores en cada llamada, el modelo "recuerda" la conversación.
# -----------------------------------------------------------------------------

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)

# El historial empieza con el system prompt y crece con cada turno
historial = [
    SystemMessage(content=(
        "Eres un experto en microcontroladores STM32. "
        "Responde de forma técnica y concisa."
    ))
]

# Conversación simulada: el ingeniero pregunta sobre DMA y hace follow-ups
TURNOS = [
    "¿Cómo funciona el DMA controller del STM32F407?",
    "¿Y cuántos streams tiene en total?",
    "¿Cuál usarías para recibir datos de UART1?",
    "Dame un ejemplo de código HAL para eso.",
]


def chat(pregunta: str) -> str:
    """Agrega la pregunta al historial, llama al modelo y guarda la respuesta."""
    historial.append(HumanMessage(content=pregunta))
    respuesta = llm.invoke(historial)
    historial.append(AIMessage(content=respuesta.content))
    return respuesta.content


if __name__ == "__main__":
    print("Conversación con historial — STM32F407 DMA\n")

    for turno, pregunta in enumerate(TURNOS, start=1):
        print(f"{'=' * 60}")
        print(f"  [{turno}] Usuario: {pregunta}")
        print("=" * 60)
        respuesta = chat(pregunta)
        print(f"  Claude: {respuesta}\n")

    # Mostrar cuántos mensajes acumuló el historial
    print(f"--- Historial final: {len(historial)} mensajes (1 system + {len(TURNOS)} pares usuario/asistente) ---")
