# Run Log

Append meaningful commands, inspections, runs, and verification outcomes here.

## 2026-04-28: Repository Scaffold

**Action:** Created the initial BabyActionLM repository scaffold.

**Result:** Pushed private GitHub repo `pragnesh-gh/baby-action-lm` on branch `main`.

**Commit:** `1ee4d42 chore: scaffold BabyActionLM project`

## 2026-04-28: Dataset Planning Inspection

**Action:** Inspected `google/mobile-actions` dataset card and viewer remotely.

**Finding:** Hugging Face exposes one `train` split with 9.65k rows. The dataset has a `metadata` field with `train` and `eval` values, `tools`, and `messages`.

**Consequence:** Implementation must split by row metadata, not by Hugging Face split.

## 2026-04-28: Local Environment Planning Inspection

**Action:** Checked local Python package availability in the bundled Codex runtime.

**Finding:** `pandas` and `numpy` are available; `torch`, `transformers`, `datasets`, `tokenizers`, `accelerate`, `pytest`, and Python `ollama` are not available there.

**Consequence:** A project environment setup step is required before dataset download, training, or tests.

## 2026-04-28: Hardware Planning Inspection

**Action:** Checked GPU with `nvidia-smi`.

**Finding:** Local GPU is NVIDIA GeForce RTX 3050 Ti Laptop GPU with 4096 MiB VRAM.

**Consequence:** Training plan starts with small smoke tests and conservative memory settings.

## 2026-04-28: Living Documentation System

**Action:** Added `AGENTS.md`, project memory, decision log, assumptions, run log, and the active implementation plan.

**Finding:** Future agents now have a documented entrypoint and update rules before dataset download or model code begins.

**Consequence:** Future work must update living docs after meaningful code, experiment, dependency, or research changes.

## 2026-04-28: Environment Validation

**Action:** Ran import and CUDA checks in Conda env `gpu-base`.

**Command:** `conda --no-plugins run -n gpu-base python -c "... import torch, transformers, datasets, tokenizers, accelerate, pytest, yaml ..."`

**Finding:** Python 3.11.11, `torch 2.5.1+cu121`, CUDA available, required training packages import successfully.

**Consequence:** `gpu-base` is the working environment for this project.

## 2026-04-28: BabyB Checkpoint Validation

**Action:** Loaded `../Assignments/Main/models/babyB/final/final` with `AutoTokenizer` and `AutoModelForCausalLM`.

**Finding:** `pad_token_id=1`, vocab size 8000, context length 128, model class `LlamaForCausalLM`.

**Consequence:** Configs use nested `final/final` checkpoint paths.

## 2026-04-28: Dataset Local Inspection

**Action:** Downloaded/loaded `google/mobile-actions` locally through Hugging Face datasets.

**Finding:** 9,654 rows total: 8,693 train and 961 eval. Rows contain `metadata`, `tools`, and `messages`; assistant tool calls are in `messages[2].tool_calls[0].function`.

**Consequence:** Full eval can use all 961 eval rows because it is below the 1000-example cap.

## 2026-04-28: Core Unit Tests

**Action:** Added parser, data, formatting, metrics, reporting, training-feature, evaluation, and Ollama adapter tests.

**Command:** `conda --no-plugins run -n gpu-base pytest -q`

**Result:** 21 tests passed.

## 2026-04-28: BabyB Smoke Fine-Tune

**Action:** Ran 32-example BabyB smoke fine-tune.

**Command:** `conda --no-plugins run -n gpu-base python -m babyactionlm.train experiments/configs/smoke.yaml`

**Result:** Completed in about 1.5 seconds of trainer runtime. Train loss `6.4386`; eval loss `6.3218`. Checkpoint saved under ignored `outputs/models/babyB-smoke`.

## 2026-04-28: BabyB Smoke Evaluation

**Action:** Evaluated the BabyB smoke checkpoint on 32 eval examples.

**Command:** `conda --no-plugins run -n gpu-base python -m babyactionlm.evaluate experiments/configs/evaluate_smoke.yaml`

**Result:** CSVs written to `results/babyB-smoke-summary.csv` and `results/babyB-smoke-per-tool.csv`. Smoke metrics: parse rate `0.0`, function accuracy `0.0`, argument exact match `0.0`, exact tool-call match `0.0`.

**Consequence:** The evaluation pipeline works; one smoke update is not enough to produce parseable Baby outputs.

## 2026-04-28: FunctionGemma Pull And Smoke Baseline

**Action:** Pulled `functiongemma:270m` and ran the 32-example Ollama baseline.

**Commands:** `ollama pull functiongemma:270m`; `conda --no-plugins run -n gpu-base python -m babyactionlm.ollama_baseline experiments/configs/functiongemma_smoke.yaml`

**Result:** `functiongemma:270m` is installed locally at about 300 MB. Smoke metrics: parse rate `0.9375`, function accuracy `0.71875`, argument exact match `0.53125`, exact tool-call match `0.53125`.

**Consequence:** The FunctionGemma baseline path works with native Ollama tool calls after schema normalization.
