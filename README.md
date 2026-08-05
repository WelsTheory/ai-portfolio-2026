# AI Portfolio — Wels

Repositorio de aprendizaje práctico en **IA Generativa y Conversational AI**.  
El objetivo es construir proyectos reales que demuestren el uso de LLMs, RAG, agentes y evaluación de prompts.

La ruta de aprendizaje está planificada pero puede ajustarse según el avance.

---

## Los 3 proyectos

### Proyecto 1 — RAG Datasheet Chatbot
Chatbot que responde preguntas sobre datasheets técnicos (STM32, PIC18F57Q43) usando Retrieval-Augmented Generation.

```
Stack: LangChain · ChromaDB · sentence-transformers · FastAPI · Streamlit · Docker
```

### Proyecto 2 — Pipeline de Evaluación de Prompts
Script que compara 4 estrategias de prompting sobre un dataset de preguntas de embedded systems.

```
Stack: Python · Claude API · RAGAS · Pandas · Matplotlib
Estrategias: Zero-Shot · Few-Shot (3-shot) · Chain-of-Thought · RAG
```

### Proyecto 3 — Agente Conversacional n8n
Agente en n8n con memoria de sesión y tool calling al RAG del Proyecto 1.

```
Stack: n8n · FastAPI · Buffer Window Memory · Webhook
```

---

## Stack general

| Componente     | Tecnología                              |
|----------------|-----------------------------------------|
| LLM (pago)     | Claude API (Haiku · Sonnet)             |
| LLM (gratis)   | Mistral API (mistral-small-latest)      |
| LLM (local)    | Qwen3 9B Q4_K_M · Llama 3.3 8B Q5_K_M  |
| Servidor local | LM Studio                               |
| Embeddings     | sentence-transformers (local)           |
| Vector DB      | ChromaDB (persistente, local)           |
| Framework      | LangChain + LangGraph                   |
| API            | FastAPI                                 |
| UI             | Streamlit                               |
| Agentes        | n8n + LangGraph                         |
| Evaluación     | RAGAS                                   |
| Contenedores   | Docker + Docker Compose                 |

---

## Hardware de desarrollo

### PC Nueva (desarrollo principal)

| Componente | Especificación |
|------------|----------------|
| CPU | AMD Ryzen 5 7500F 6-Core (3.70 GHz) |
| GPU | NVIDIA RTX 5060 — 8GB VRAM |
| RAM | 32GB |
| Storage | 2.22 TB (580 GB libres) |
| Modelos locales | Qwen3 9B Q4_K_M · Llama 3.3 8B Instruct Q5_K_M |

### PC Antigua (servidor/backup)

| Componente | Especificación |
|------------|----------------|
| CPU | AMD Ryzen 5 2600 (6 cores, 12 threads) |
| GPU | NVIDIA GTX 1050 Ti — 4GB VRAM |
| RAM | 15GB |
| Storage | 720 GB libres |
| Modelos locales | TinyLlama 1.1B |

---

## Setup

### 1. Clonar y crear entorno virtual

```bash
git clone <repo>
cd IA_Roadmap

python3.12 -m venv .venv

# Windows (PowerShell)
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar API key

Copiar `.env.example` a `.env` y completar los valores:

```bash
# Linux / macOS
cp .env.example .env

# Windows (PowerShell)
copy .env.example .env
```

### 4. Verificar

```bash
python semana01/hello_claude.py
```

---

## Estructura del repositorio

```
IA_Roadmap/
├── semana01/               ← Fundamentos + primera llamada a Claude API
├── semana02/               ← LangChain + LCEL
├── semana03/               ← Agentes + ReAct
├── semana04/               ← LangGraph + Multi-agente
├── semana05-08/            ← Proyecto 1: RAG Datasheet Chatbot
├── semana08-09/            ← Proyecto 2: Evaluación de Prompts
├── semana09-10/            ← Proyecto 3: Agente n8n
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```
