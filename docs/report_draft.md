# BabyActionLM Report Draft

## Current Status

The implementation now supports the core experimental pipeline: Mobile Actions records can be loaded, formatted into compact BabyLM prompts and JSON tool-call targets, parsed back into canonical tool calls, scored with shared metrics, and written to report-ready CSV files.

## Planned Result Table

The final report should compare BabyA, BabyB, and `functiongemma:270m` on the same eval IDs with:

- parse rate
- function accuracy
- argument exact match
- exact tool-call match
- per-tool breakdown

## Interpretation Frame

BabyA and BabyB test the BabyLM pretraining question. FunctionGemma is a practical edge function-calling reference point, not a same-size baseline. The project remains a simulated NLP tool-call parsing experiment rather than an Android app.
