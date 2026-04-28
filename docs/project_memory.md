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

Current full-eval results on 961 examples:

- BabyA: parse `0.0187`, function accuracy `0.0031`, exact tool-call match `0.0`.
- BabyB: parse `0.3559`, function accuracy `0.0531`, exact tool-call match `0.0`.
- FunctionGemma: parse `0.9813`, function accuracy `0.7097`, exact tool-call match `0.4964`.

## Current Repository State

- Repository: `pragnesh-gh/baby-action-lm`
- Branch: `babyactionlm-core`
- Initial scaffold is pushed to GitHub.
- Core package, tests, configs, full BabyA/B fine-tuning/evaluation, full FunctionGemma evaluation, plots, and qualitative examples are implemented locally.
- Tracked result CSVs and figures exist under `results/`; raw predictions and checkpoints are ignored under `outputs/`.

## Active Implementation Plan

Use `docs/superpowers/plans/2026-04-28-babyactionlm-implementation.md`.

For the human-readable project flow, use `docs/project_flow.md`.

For the versioned roadmap, use `docs/version_roadmap.md`.

## Next Actions

1. Interpret the full v1 results in `docs/report_draft.md`.
2. Decide whether to run a v1.5 prompt/training cleanup because BabyA/B exact-match remains `0.0`.
3. If doing v1.5, try a parse-friendlier target/prompt while keeping the same eval split and metrics.
4. If staying with v1, turn the current tables, plots, and qualitative examples into the final course report.

## Open Questions

- Whether v1.5 should change the prompt/target format to improve Baby parseability.
- Whether a scratch tiny model is worth the extra time after BabyA/B and FunctionGemma are already compared.
- How to frame the result: BabyB clearly improves over BabyA on parseability, but both are far from reliable exact tool-call controllers.
