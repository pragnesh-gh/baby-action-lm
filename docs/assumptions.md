# Assumptions

Last updated: 2026-04-29

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
- v1.5 should be treated as diagnostic evidence unless it clearly improves several metrics at once.

## Assumptions To Validate

- Whether an unfine-tuned BabyA/B baseline would add enough value to justify the runtime.
- Whether a scratch tiny model is needed for the final course report.
- Whether v2 should focus on a control model, a prompt ablation, or an error taxonomy rather than more epoch tuning.

## Validated Assumptions

- The dataset's `metadata` field provides train/eval labels: 8,693 train rows and 961 eval rows.
- BabyA and BabyB load with Hugging Face `transformers` as LLaMA causal language models.
- The canonical BabyB checkpoint has `pad_token_id=1`, vocab size 8000, and `max_position_embeddings=128`.
- The RTX 3050 Ti 4 GB GPU can run a 32-example BabyB smoke fine-tune locally.
- Ollama `functiongemma:270m` can be pulled and evaluated locally on a 32-example smoke set.
- The final eval split is small enough to use all 961 eval examples for BabyA/B; the 1000-example cap remains a guardrail.
- Full BabyA/B fine-tuning completes locally without out-of-memory errors.
- Full FunctionGemma evaluation over 961 eval rows completes locally.
- BabyB has a measurable advantage over BabyA after task fine-tuning on parse rate and function accuracy.
- Fine-tuning improves BabyB parseability enough to study errors, but v1 does not achieve exact tool-call matches for BabyA/B.
- The v1 `trainer_state.json` files are sufficient to retroactively generate train/eval loss curves.
- A train/dev split from `metadata=train` is reproducible with seed 42 and can be used for v1.5 selection.
- DSL-3 gives BabyB a tiny nonzero exact-match signal on dev and official eval, but it does not make the Baby model practically reliable.
- Longer v1.5 training is not automatically better: JSON-8 improves parse/function scores but not exact match, while DSL-8 loses the DSL-3 exact-match signal.
