from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --- 1. Prompt template con variable {topic} ---
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un experto en microcontroladores STM32. "
        "Responde de forma concisa y técnica, con ejemplos de código HAL cuando sea útil.",
    ),
    ("human", "Explícame brevemente: {topic}"),
])

# --- 2. Modelo ---
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)

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
    for tema in TEMAS:
        print(f"\n{'=' * 60}")
        print(f"  TEMA: {tema}")
        print("=" * 60)
        result = chain.invoke({"topic": tema})
        print(result)
