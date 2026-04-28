# BabyActionLM Project Memory

Last updated: 2026-04-28

## Current Thesis

A BabyLM-scale language model may not be a general assistant, but it may be useful as a local, private, low-latency controller for simple mobile-agent actions. The project tests whether small pretrained language models can translate user phone commands into structured function calls.

## Research Question

Can BabyLM-style pretraining help a very small neural language model learn reliable mobile action parsing?

Secondary questions:

- Can a tiny model output parseable JSON-style tool calls?
- Does BabyB, pretrained on more text than BabyA, outperform BabyA after task fine-tuning?
- How far are BabyA/B from zero-shot `functiongemma:270m` on the same evaluation examples?

## Current Experiment Design

Dataset:

- `google/mobile-actions` from Hugging Face.
- The dataset has one HF split named `train`; the real train/eval distinction is in the `metadata` field.
- Local inspection found 9,654 rows: 8,693 `train` and 961 `eval`.
- Each row contains 7 available tools and a 3-message trace: developer context, user command, assistant tool call.
- The canonical target is compact JSON: `{"name":"tool_name","arguments":{...}}`.
- The Baby prompt is compact: task instruction, semicolon-separated tool signatures, command, then `JSON:`.

Models:

- BabyA checkpoint: `../Assignments/Main/models/babyA/final/final`
- BabyB checkpoint: `../Assignments/Main/models/babyB/final/final`
- Optional scratch tiny LLaMA-style control after BabyA/B are working.
- Zero-shot baseline: `functiongemma:270m` through Ollama.

Evaluation:

- Parse rate.
- Function accuracy.
- Argument exact match.
- Exact tool-call match.
- Per-tool breakdown and qualitative error examples.

## Current Repository State

- Repository: `pragnesh-gh/baby-action-lm`
- Branch: `babyactionlm-core`
- Initial scaffold is pushed to GitHub.
- Core package, tests, configs, smoke fine-tune, smoke evaluation, and FunctionGemma smoke baseline are implemented locally.
- Tracked smoke result CSVs exist under `results/`; raw predictions and checkpoints are ignored under `outputs/`.

## Active Implementation Plan

Use `docs/superpowers/plans/2026-04-28-babyactionlm-implementation.md`.

## Next Actions

1. Review smoke outputs and decide whether to tune the prompt before full BabyA/B training.
2. Run full BabyB fine-tuning with `experiments/configs/babyB.yaml`.
3. Run full BabyA fine-tuning with `experiments/configs/babyA.yaml`.
4. Evaluate BabyA/B on the full 961-example eval split.
5. Optionally run full FunctionGemma eval with `experiments/configs/functiongemma_zero_shot.yaml`.

## Open Questions

- Whether the compact Baby prompt should include richer tool descriptions after checking token coverage.
- Whether 3 epochs are enough for BabyA/B full fine-tuning.
- Whether FunctionGemma full eval runtime is acceptable; smoke-32 took about one minute.
