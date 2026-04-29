# BabyActionLM Version Roadmap

This roadmap keeps the project from becoming vague after v1. v1 and v1.5 are now implemented; later versions are optional strengthening paths.

## v1: Working Scientific Baseline

Goal: prove the full experiment works.

- Fine-tune BabyA and BabyB on Mobile Actions.
- Evaluate both on the same eval examples.
- Compare with `functiongemma:270m`.
- Produce tables, plots, and qualitative examples.
- Write a report around the core thesis: does BabyLM-style pretraining help tiny mobile tool-call parsing?

Status: implemented. The pipeline runs end to end and produces defensible metrics, even though BabyA/B are weak.

## v1.5: Make The Baseline Fairer

Goal: improve v1 if BabyA/B fail mostly because of formatting rather than model capacity.

- Try a slightly different compact prompt/target format.
- Adjust epochs.
- Check token-length coverage.
- Simplify target format only if JSON proves too hard.

Status: implemented as JSON-3, JSON-8, DSL-3, and DSL-8 BabyB dev trials, followed by final DSL-3 BabyA/B eval.

Outcome: DSL-3 gave BabyB a tiny nonzero exact-match score, but JSON v1 remains better for BabyB parse and function accuracy. v1.5 is diagnostic evidence, not a full fix.

## v2: Stronger Pretraining Comparison

Goal: make the scientific claim sharper.

- Add an unfine-tuned BabyA/B evaluation if useful.
- Add a scratch tiny model only if time allows.
- Compare BabyA vs BabyB vs scratch vs FunctionGemma.
- Analyze whether more BabyLM pretraining improves downstream action parsing.

Success: the report can say more than "the pipeline works"; it can discuss evidence for or against the pretraining hypothesis.

## v3: Richer Analysis

Goal: make the evaluation feel research-grade.

- Per-tool difficulty analysis.
- Error taxonomy: malformed JSON, wrong tool, missing required args, extra args, date/time mistakes.
- Data-size ablation: train with 100, 500, 1000, full examples.
- Prompt ablation: tool signatures vs richer tool descriptions.

Success: the project has depth even if absolute BabyA/B scores are modest.

## v4: Demo Layer

Goal: make the result tangible, not just a table.

- Add a small CLI demo that accepts a command and prints the predicted tool call.
- Keep actions simulated.
- Do not build an Android app unless the course scope changes.

Success: someone can try the trained model locally and understand the task intuitively.
