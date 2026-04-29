# BabyActionLM Project Memory

Last updated: 2026-04-29

## Current Thesis

A BabyLM-scale language model may not be a general assistant, but it may be useful as a local, private, low-latency controller for simple mobile-agent actions. The project tests whether small pretrained language models can translate user phone commands into structured function calls.

## Research Question

Can BabyLM-style pretraining help a very small neural language model learn reliable mobile action parsing?

Secondary questions:

- Can a tiny model output parseable structured tool calls?
- Does BabyB, pretrained on more text than BabyA, outperform BabyA after task fine-tuning?
- How far are BabyA/B from zero-shot `functiongemma:270m` on the same evaluation examples?

## Current Experiment Design

Dataset:

- `google/mobile-actions` from Hugging Face.
- The dataset has one HF split named `train`; the real train/eval distinction is in the `metadata` field.
- Local inspection found 9,654 rows: 8,693 `train` and 961 `eval`.
- Each row contains 7 available tools and a 3-message trace: developer context, user command, assistant tool call.
- v1 target format is compact JSON: `{"name":"tool_name","arguments":{...}}`.
- v1.5 also tests a compact DSL target: `tool=tool_name;arg=value`, normalized into the same `ToolCall` schema.
- Baby prompts are compact: task instruction, semicolon-separated tool signatures, command, then either `JSON:` or `TOOL:`.

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
- BabyA v1.5 DSL-3: parse `0.3632`, function accuracy `0.0`, exact tool-call match `0.0`.
- BabyB v1.5 DSL-3: parse `0.1145`, function accuracy `0.0083`, exact tool-call match `0.0073`.

v1.5 selection used only a held-out dev split from `metadata=train`. The best BabyB dev trial was `dsl_v1` for 3 epochs because it was the only trial with nonzero exact tool-call match. The official 961-example eval split was kept for final reporting.

## Current Repository State

- Repository: `pragnesh-gh/baby-action-lm`
- Branch: `babyactionlm-core`
- Initial scaffold is pushed to GitHub.
- Core package, tests, configs, full BabyA/B v1 fine-tuning/evaluation, FunctionGemma evaluation, v1.5 DSL trialing, plots, and qualitative examples are implemented locally.
- Tracked result CSVs and figures exist under `results/`; raw predictions and checkpoints are ignored under `outputs/`.

## Active Implementation Plan

Use `docs/superpowers/plans/2026-04-28-babyactionlm-implementation.md` and `docs/superpowers/plans/2026-04-29-babyactionlm-v15.md`.

For the human-readable project flow, use `docs/project_flow.md`.

For the versioned roadmap, use `docs/version_roadmap.md`.

## Next Actions

1. Run final verification and commit/push the v1.5 artifacts.
2. Turn `docs/report_draft.md`, `results/summary.csv`, `results/v15_trials.csv`, and the figures into the final course report.
3. Decide whether to stop at v1.5 or add a v2 control such as an unfine-tuned BabyB or scratch tiny model.

## Open Questions

- Whether a scratch tiny model is worth the extra time after BabyA/B and FunctionGemma are already compared.
- How to frame v1.5: the DSL format gives BabyB a tiny nonzero exact-match signal, but it is not a practical controller and does not beat the v1 JSON parse/function scores.
