# Assumptions

Last updated: 2026-04-28

## Fixed Assumptions

- This is a Neural Networks for NLP course project.
- The project is an NLP experiment, not an Android application.
- Phone actions are simulated through structured function-call outputs.
- Raw datasets, model weights, checkpoints, logs, and generated caches stay out of git.
- BabyA and BabyB checkpoints live outside this repo under `../Assignments/Main/models/`.
- FunctionGemma is a zero-shot baseline unless a future decision changes that.

## Working Assumptions

- `google/mobile-actions` is suitable as the main dataset.
- The dataset's `metadata` field provides train/eval labels.
- BabyA and BabyB can be loaded with Hugging Face `transformers` as LLaMA causal language models.
- The RTX 3050 Ti 4 GB GPU can run tiny-model smoke tests locally.
- Full fine-tuning may need conservative batch sizes, gradient accumulation, and fp16.
- Prompt compression may be needed if full tool descriptions exceed the tiny model context window.

## Assumptions To Validate

- The full Mobile Actions prompt/target format fits within practical `max_length` settings.
- Fine-tuning on Mobile Actions improves parse rate and exact match over unfine-tuned BabyA/B.
- BabyB has a measurable advantage over BabyA after task fine-tuning.
- Ollama `functiongemma:270m` can be pulled and evaluated locally at acceptable speed.
- A capped or stratified eval subset is enough if full FunctionGemma evaluation is slow.

