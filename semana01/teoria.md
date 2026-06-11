# Semana 1 — Teoría: Fundamentos de LLMs

## Transformers — la arquitectura base

Un LLM es una red neuronal entrenada para predecir el siguiente token dado un contexto. La innovación del Transformer (2017) fue el mecanismo de **atención**: en lugar de procesar texto secuencialmente, procesa todos los tokens **en paralelo** y calcula qué tan relevante es cada token para cada otro.

> Analogía: imagina un bus SPI donde todos los dispositivos escuchan al mismo tiempo y cada uno decide cuánto "peso" le da al mensaje del maestro. Eso es atención.

---

## Tokenización

El texto no entra como caracteres ni palabras enteras — entra como **tokens**, fragmentos de palabras.

```
"STM32F407" → ["ST", "M", "32", "F", "407"]   # ~5 tokens
"DMA"       → ["DMA"]                           # 1 token
```

Cada token se convierte en un número (su ID en el vocabulario). El modelo nunca ve texto — solo ve secuencias de enteros.

Regla práctica: **1 token ≈ 0.75 palabras en inglés**. En español es un poco más por tildes y morfología.

---

## Embeddings

Un token ID es solo un número. El embedding lo convierte en un **vector de alta dimensión** (ej: 768 o 4096 números) donde la posición en ese espacio tiene significado semántico.

```
"timer"    → [0.21, -0.83, 0.44, ...]
"counter"  → [0.19, -0.79, 0.41, ...]   ← cerca en el espacio vectorial
"FreeRTOS" → [0.67,  0.12, -0.55, ...]  ← lejos
```

> Analogía: como una tabla de lookup en flash, pero en lugar de devolver un valor devuelve un vector de 768 dimensiones que codifica el "significado" del token.

---

## Flujo completo de una llamada a la API

```
tu texto
    ↓ tokenizer
[IDs de tokens]
    ↓ embedding layer
[vectores]
    ↓ N capas Transformer (atención + feed-forward)
[vector final]
    ↓ cabeza de clasificación
probabilidades sobre vocabulario
    ↓ sampling
siguiente token → repetir hasta max_tokens o [EOS]
```

Cada vez que ves `max_tokens=512` en el código, estás limitando cuántas veces corre ese loop.

---

## IA Responsable — lo esencial

| Riesgo | Descripción | Acción |
|--------|-------------|--------|
| Alucinaciones | El modelo genera el token más probable, no el más verdadero | En datasheets técnicos, siempre verificar contra la fuente original |
| Sesgos | Hereda los sesgos de sus datos de entrenamiento | Validar respuestas críticas |
| Datos sensibles | APIs externas pueden almacenar los prompts | Nunca enviar información confidencial sin revisar los términos de uso |

---

## Recursos para profundizar

- [3Blue1Brown — Neural Networks](https://youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
- [Andrej Karpathy — Intro to LLMs](https://youtu.be/zjkBMFhNj_g) (1 hora)
