import time
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Versión gratuita de chain_basica.py usando Mistral en lugar de Claude
# Mismo patrón LCEL — solo cambia el modelo
# Requiere: pip install langchain-mistralai

# --- 1. Prompt template ---
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un experto en microcontroladores STM32. "
        "Responde de forma concisa y técnica, con ejemplos de código HAL cuando sea útil.",
    ),
    ("human", "Explícame brevemente: {topic}"),
])

# --- 2. Modelo ---
llm = ChatMistralAI(model="mistral-small-latest", max_tokens=512)

# --- 3. Output parser ---
parser = StrOutputParser()

# --- 4. Chain con LCEL (pipe syntax) ---
chain = prompt | llm | parser

# --- 5. Invocaciones ---
TEMAS = [
    "cómo funciona el DMA controller y cuándo usarlo",
    "diferencia entre TIM2 y TIM6 en el STM32F407",
    "cómo configurar UART con HAL en modo receive IT",
]

if __name__ == "__main__":
    for i, tema in enumerate(TEMAS):
        print(f"\n{'=' * 60}")
        print(f"  TEMA: {tema}")
        print("=" * 60)
        result = chain.invoke({"topic": tema})
        print(result)
        # Pausa entre llamadas para respetar el rate limit del tier gratuito
        if i < len(TEMAS) - 1:
            time.sleep(3)
