# Reading Notes

## GPT-wee / BabyLM

**Citation:** Bastian Bunzeck and Sina Zarriess. 2023. GPT-wee: How Small Can a Small Language Model Really Get?

**Use in this project:** Motivates BabyLM-scale models and small-data language modeling. Provides the course-local foundation for using tiny language models rather than large general assistants.

## TinyAgent

**Citation:** Lutfi Eren Erdogan et al. 2024. TinyAgent: Function Calling at the Edge.

**Use in this project:** Closest ACL reference for task-specific small language model agents capable of function calling at the edge. BabyActionLM is a smaller course-scale version using BabyLM checkpoints and a mobile-actions dataset.

## Toolformer

**Citation:** Timo Schick et al. 2023. Toolformer: Language Models Can Teach Themselves to Use Tools.

**Use in this project:** Broader framing for API/tool use as a language modeling problem. BabyActionLM focuses on the output side: selecting a phone action and arguments.

## FunctionGemma and Mobile Actions

**Sources:** Google FunctionGemma docs, Google Mobile Actions dataset, Ollama `functiongemma:270m`.

**Use in this project:** Provides the modern edge baseline and dataset for structured phone action parsing.
