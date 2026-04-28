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
- Full fine-tuning may need conservative batch sizes, gradient accumulation, and fp16.
- Prompt compression may be needed if full tool descriptions exceed the tiny model context window.
- Three full fine-tuning epochs may be enough for the first BabyA/B comparison.

## Assumptions To Validate

- Fine-tuning on Mobile Actions improves parse rate and exact match over unfine-tuned BabyA/B.
- BabyB has a measurable advantage over BabyA after task fine-tuning.
- Full BabyA/B fine-tuning completes locally without out-of-memory errors.
- Full FunctionGemma evaluation over 961 eval rows completes at acceptable speed.

## Validated Assumptions

- The dataset's `metadata` field provides train/eval labels: 8,693 train rows and 961 eval rows.
- BabyA and BabyB load with Hugging Face `transformers` as LLaMA causal language models.
- The canonical BabyB checkpoint has `pad_token_id=1`, vocab size 8000, and `max_position_embeddings=128`.
- The RTX 3050 Ti 4 GB GPU can run a 32-example BabyB smoke fine-tune locally.
- Ollama `functiongemma:270m` can be pulled and evaluated locally on a 32-example smoke set.
- The final eval split is small enough to use all 961 eval examples for BabyA/B; the 1000-example cap remains a guardrail.
