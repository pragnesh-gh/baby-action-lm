# BabyActionLM v1.5 Implementation Plan

## Goal

Test whether BabyA/B failed exact tool-call matching in v1 mainly because compact JSON was hard to generate, or because the tiny models lack enough task capacity.

## Protocol

1. Generate training curves from saved v1 Hugging Face `trainer_state.json` logs.
2. Split `metadata=train` into train/dev with seed 42.
3. Keep the official 961 `metadata=eval` rows untouched until final evaluation.
4. Compare BabyB variants on dev:
   - `json_v1`, 3 epochs
   - `json_v1`, 8 epochs
   - `dsl_v1`, 3 epochs
   - `dsl_v1`, 8 epochs
5. Select by exact tool-call match, then function accuracy, then parse rate.
6. Train/evaluate BabyA and BabyB with the selected setup on official eval.
7. Rebuild summary tables, per-tool tables, training curves, metric plots, and qualitative examples.

## Implemented Outcome

`babyB-v15-dsl-3` was selected on dev because it was the only trial with nonzero exact tool-call match. Official eval results:

- BabyA v1.5 DSL-3: parse `0.3632`, function `0.0`, exact `0.0`.
- BabyB v1.5 DSL-3: parse `0.1145`, function `0.0083`, exact `0.0073`.

## Interpretation

v1.5 supports a narrow format-sensitivity claim: flattening the output can produce a small exact-match signal for BabyB. It does not make BabyA/B reliable controllers, and it does not dominate v1 JSON on parse/function metrics.
