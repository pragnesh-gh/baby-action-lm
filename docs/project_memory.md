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
- Each row contains 7 available tools and a 3-message trace: developer context, user command, assistant tool call.

Models:

- BabyA checkpoint: `../Assignments/Main/models/babyA/final`
- BabyB checkpoint: `../Assignments/Main/models/babyB/final`
- Optional scratch tiny LLaMA-style control after BabyA/B are working.
- Zero-shot baseline: `functiongemma:270m` through Ollama.

Evaluation:

- Parse rate.
- Function accuracy.
- Argument accuracy.
- Exact tool-call match.
- Per-tool breakdown and qualitative error examples.

## Current Repository State

- Repository: `pragnesh-gh/baby-action-lm`
- Branch: `main`
- Initial scaffold is pushed to GitHub.
- Living documentation system has been added before dataset download or model code.

## Active Implementation Plan

Use `docs/superpowers/plans/2026-04-28-babyactionlm-implementation.md`.

## Next Actions

1. Install project dependencies in an environment suitable for CUDA training.
2. Pull `functiongemma:270m` with Ollama.
3. Implement dataset loading, splitting, and prompt/target formatting.
4. Add parser and metric tests before model work.
5. Run a 32-example smoke test before full fine-tuning.

## Open Questions

- Whether max sequence length 128 is enough for all Mobile Actions prompts, or whether 256 is needed.
- Whether RTX 3050 Ti 4 GB VRAM can fine-tune with full prompts, or whether prompt compression is required.
- Whether FunctionGemma should be evaluated on the full eval subset or a stratified capped subset for runtime.
