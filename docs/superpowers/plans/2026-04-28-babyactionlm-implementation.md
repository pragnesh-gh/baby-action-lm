# BabyActionLM Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible BabyActionLM experiment that fine-tunes BabyA/B tiny BabyLM checkpoints on Mobile Actions and evaluates structured mobile tool-call parsing against `functiongemma:270m`.

**Architecture:** The project is a Python package with isolated data, formatting, parsing, metric, training, and baseline modules. Large artifacts stay local and ignored. Small summaries and report-ready results are tracked.

**Tech Stack:** Python, Hugging Face `datasets`, `transformers`, `tokenizers`, PyTorch, Ollama, pandas, pytest.

---

## Stage 1: Environment And Dataset Access

### Task 1: Create A Reproducible Environment

**Files:**

- Modify: `requirements.txt`
- Update: `docs/run_log.md`
- Update: `docs/project_memory.md`

- [ ] Confirm the target Python environment.
- [ ] Install dependencies with `pip install -r requirements.txt`.
- [ ] Verify imports for `torch`, `transformers`, `datasets`, `tokenizers`, `accelerate`, `pandas`, `pytest`, and `ollama`.
- [ ] Record the environment command and result in `docs/run_log.md`.

### Task 2: Pull The FunctionGemma Baseline

**Files:**

- Update: `docs/run_log.md`
- Update: `docs/assumptions.md`

- [ ] Run `ollama pull functiongemma:270m`.
- [ ] Run `ollama list` and confirm `functiongemma:270m` is present.
- [ ] Record the model availability and size in `docs/run_log.md`.
- [ ] Move the FunctionGemma availability assumption from "to validate" to confirmed in `docs/assumptions.md`.

## Stage 2: Dataset Loading And Formatting

### Task 3: Implement Dataset Loader

**Files:**

- Create: `src/babyactionlm/__init__.py`
- Create: `src/babyactionlm/data.py`
- Create: `tests/test_data.py`
- Update: `docs/run_log.md`

- [ ] Add a loader that calls `load_dataset("google/mobile-actions", split="train")`.
- [ ] Split rows into train/eval by `row["metadata"]`.
- [ ] Return lightweight records with `id`, `split`, `tools`, and `messages`.
- [ ] Add tests using synthetic rows so tests do not require network access.
- [ ] Run `pytest tests/test_data.py -v`.

### Task 4: Implement Prompt And Target Formatting

**Files:**

- Create: `src/babyactionlm/formatting.py`
- Create: `tests/test_formatting.py`
- Update: `docs/project_memory.md`

- [ ] Extract developer context from `messages[0].content`.
- [ ] Extract user command from `messages[1].content`.
- [ ] Extract gold tool call from `messages[2].tool_calls[0].function`.
- [ ] Format targets as compact JSON: `{"name":"...","arguments":{...}}`.
- [ ] Use one canonical prompt template for BabyA/B and document it in `docs/project_memory.md`.
- [ ] Run `pytest tests/test_formatting.py -v`.

## Stage 3: Parser And Metrics

### Task 5: Implement Tool-Call Parser

**Files:**

- Create: `src/babyactionlm/schema.py`
- Create: `tests/test_schema.py`

- [ ] Parse valid JSON model output into canonical `name` and `arguments`.
- [ ] Normalize stringified JSON arguments when present.
- [ ] Drop keys with `null` values from arguments.
- [ ] Return a parse-failure object for malformed output instead of crashing.
- [ ] Run `pytest tests/test_schema.py -v`.

### Task 6: Implement Evaluation Metrics

**Files:**

- Create: `src/babyactionlm/metrics.py`
- Create: `tests/test_metrics.py`

- [ ] Compute parse rate.
- [ ] Compute function accuracy over all examples.
- [ ] Compute required-argument accuracy.
- [ ] Compute exact tool-call match.
- [ ] Compute per-tool summaries.
- [ ] Run `pytest tests/test_metrics.py -v`.

## Stage 4: BabyA/B Fine-Tuning

### Task 7: Implement Tiny Model Training Script

**Files:**

- Create: `src/babyactionlm/train.py`
- Create: `experiments/configs/smoke.yaml`
- Create: `experiments/configs/babyA.yaml`
- Create: `experiments/configs/babyB.yaml`
- Update: `docs/run_log.md`

- [ ] Load BabyA/B checkpoints from `../Assignments/Main/models/babyA/final` and `../Assignments/Main/models/babyB/final`.
- [ ] Tokenize prompt plus target for causal LM fine-tuning.
- [ ] Mask prompt tokens in labels so loss is applied only to target tokens.
- [ ] Use conservative defaults for 4 GB VRAM: small batch size, gradient accumulation, fp16 when CUDA is available, and checkpoint saving outside git.
- [ ] Run the smoke config before full training.
- [ ] Record runtime, memory issues, and output directories in `docs/run_log.md`.

### Task 8: Implement Tiny Model Evaluation Script

**Files:**

- Create: `src/babyactionlm/evaluate.py`
- Update: `docs/run_log.md`

- [ ] Load a fine-tuned model output directory.
- [ ] Generate tool-call predictions for eval records.
- [ ] Save raw predictions under ignored `outputs/`.
- [ ] Save small summaries under tracked `results/`.
- [ ] Run smoke evaluation on 32 examples before full eval.

## Stage 5: FunctionGemma Baseline

### Task 9: Implement Ollama Baseline

**Files:**

- Create: `src/babyactionlm/ollama_baseline.py`
- Create: `experiments/configs/functiongemma_zero_shot.yaml`
- Update: `docs/run_log.md`

- [ ] Call local Ollama with model `functiongemma:270m`.
- [ ] Use the same eval IDs as BabyA/B.
- [ ] Parse FunctionGemma outputs through the same schema and metrics code.
- [ ] Save raw predictions under ignored `outputs/`.
- [ ] Save summary CSV under tracked `results/`.

## Stage 6: Reporting And Handoff

### Task 10: Create Result Summary And Report Draft

**Files:**

- Create: `results/summary.csv`
- Create: `results/per_tool.csv`
- Create: `docs/report_draft.md`
- Update: `docs/project_memory.md`
- Update: `docs/decision_log.md`

- [ ] Compare BabyA, BabyB, optional scratch, and FunctionGemma.
- [ ] Include parse rate, function accuracy, argument accuracy, exact match, and per-tool metrics.
- [ ] Add qualitative error examples.
- [ ] Update the project memory with final experiment status.
- [ ] Record any new interpretation decisions in the decision log.

## Verification Before Handoff

- [ ] Run all available tests with `pytest`.
- [ ] Run `git status --short --branch`.
- [ ] Verify `docs/project_memory.md` reflects the current implementation stage.
- [ ] Verify every new design decision is appended to `docs/decision_log.md`.
- [ ] Verify every major experiment command is appended to `docs/run_log.md`.
- [ ] Push committed changes to `origin/main` when the user asks for the completed stage to be published.

