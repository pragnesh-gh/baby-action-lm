# Project Scope

## In Scope

- Study language-to-tool-call parsing as a neural NLP task.
- Use the `google/mobile-actions` dataset.
- Fine-tune existing BabyA and BabyB tiny LLaMA-style BabyLM checkpoints from the course work.
- Evaluate structured outputs with parse rate, function accuracy, argument accuracy, and exact match.
- Compare with `functiongemma:270m` through Ollama as a zero-shot edge-model baseline.
- Produce a short academic report and presentation-ready results.

## Out of Scope

- Building an Android application.
- Running real phone actions.
- Collecting private phone data.
- Training or fine-tuning multi-billion-parameter models.
- Deploying to Google AI Edge Gallery as a required deliverable.
- Making claims about production reliability or safety.

## Success Criteria

The project is successful if it produces:

- a reproducible dataset preparation and evaluation flow
- fine-tuned BabyA/B model results on Mobile Actions
- a FunctionGemma baseline result on the same evaluation examples
- an analysis of whether BabyLM pretraining helps
- a concise final report grounded in BabyLM and edge-agent literature

## Default Experimental Shape

- Use official metadata split from `google/mobile-actions` where possible.
- If the eval split is large, use a stratified 1000-example eval subset.
- Run a smaller smoke test before full fine-tuning.
- Track only small result files in git.
- Keep models, datasets, checkpoints, and logs out of git.

