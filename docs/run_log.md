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

## 2026-04-28: Project Flow And Version Roadmap

**Action:** Added `docs/project_flow.md` and `docs/version_roadmap.md`.

**Finding:** v1 is the course deliverable; v1.5 through v4 are optional strengthening paths.

**Consequence:** Future sessions should use these docs to avoid re-discussing the overall flow from scratch.

## 2026-04-28: Full BabyB Fine-Tune And Eval

**Action:** Fine-tuned BabyB on the full Mobile Actions training split and evaluated on all 961 eval examples.

**Commands:** `conda --no-plugins run -n gpu-base python -m babyactionlm.train experiments/configs/babyB.yaml`; `conda --no-plugins run -n gpu-base python -m babyactionlm.evaluate experiments/configs/evaluate_babyB.yaml`

**Result:** Final training eval loss `1.4563`. Full eval metrics: parse rate `0.3559`, function accuracy `0.0531`, argument exact match `0.0`, exact tool-call match `0.0`.

**Consequence:** BabyB learned to produce parseable fragments much more often than BabyA, but not reliable exact tool calls under v1 formatting.

## 2026-04-28: Full BabyA Fine-Tune And Eval

**Action:** Fine-tuned BabyA with the same settings and evaluated on all 961 eval examples.

**Commands:** `conda --no-plugins run -n gpu-base python -m babyactionlm.train experiments/configs/babyA.yaml`; `conda --no-plugins run -n gpu-base python -m babyactionlm.evaluate experiments/configs/evaluate_babyA.yaml`

**Result:** Final training eval loss `2.3431`. Full eval metrics: parse rate `0.0187`, function accuracy `0.0031`, argument exact match `0.0`, exact tool-call match `0.0`.

**Consequence:** BabyA is much weaker than BabyB on this task, supporting the idea that the stronger BabyLM pretraining helps.

## 2026-04-28: Full FunctionGemma Eval

**Action:** Evaluated `functiongemma:270m` with native Ollama tool calls on all 961 eval examples.

**Command:** `conda --no-plugins run -n gpu-base python -m babyactionlm.ollama_baseline experiments/configs/functiongemma_zero_shot.yaml`

**Result:** Full eval metrics: parse rate `0.9813`, function accuracy `0.7097`, argument exact match `0.5099`, exact tool-call match `0.4964`.

**Consequence:** FunctionGemma is far stronger than BabyA/B and provides a useful practical ceiling/reference point.

## 2026-04-28: Analysis Artifacts

**Action:** Built combined result tables, plots, and qualitative examples.

**Command:** `conda --no-plugins run -n gpu-base python -m babyactionlm.analysis`

**Result:** Created `results/summary.csv`, `results/per_tool.csv`, `results/figures/metric_comparison.png`, `results/figures/per_tool_exact_match.png`, and `results/qualitative_examples.md`.

**Consequence:** The project now has quantitative and qualitative artifacts for the report.

## 2026-04-29: v1 Training Curves

**Action:** Extracted trainer histories from saved v1 BabyA/B checkpoints and regenerated the training-curve plot.

**Command:** `conda --no-plugins run -n gpu-base python -m babyactionlm.training_history`

**Result:** Created `results/training_history.csv` and `results/figures/training_curves.png`. The final version also includes selected v1.5 DSL-3 BabyA/B histories.

**Consequence:** The report can show that loss improved during fine-tuning even when exact tool-call accuracy stayed weak.

## 2026-04-29: v1.5 Trial Implementation Tests

**Action:** Added DSL parsing/formatting, train/dev splitting, trainer-history extraction, and trial-selection tests.

**Command:** `conda --no-plugins run -n gpu-base pytest tests/test_schema.py tests/test_v15.py -q -o addopts='-p no:cacheprovider'`

**Result:** 8 focused tests passed after fixing DSL parsing to tolerate generated prefixes such as `TOOL: tool=...`.

**Consequence:** DSL outputs and trial selection are covered before full v1.5 runs.

## 2026-04-29: v1.5 BabyB Dev Trials

**Action:** Ran four BabyB v1.5 train/eval trials on a held-out dev split from `metadata=train`.

**Commands:** `python -m babyactionlm.train experiments/configs/v15_babyB_json_3.yaml`; `python -m babyactionlm.evaluate experiments/configs/evaluate_v15_babyB_json_3_dev.yaml`; repeated for JSON-8, DSL-3, and DSL-8.

**Result:** `results/v15_trials.csv` selected `babyB-v15-dsl-3`. Dev metrics:

- JSON-3: parse `0.1940`, function `0.0253`, exact `0.0`.
- JSON-8: parse `0.3123`, function `0.0505`, exact `0.0`.
- DSL-3: parse `0.1068`, function `0.0115`, exact `0.0080`.
- DSL-8: parse `0.0907`, function `0.0149`, exact `0.0`.

**Consequence:** v1.5 selection favored exact tool-call match first, so DSL-3 became the final setup despite weaker parse/function scores.

## 2026-04-29: v1.5 Official Evaluation

**Action:** Trained BabyA with the selected DSL-3 setup, reused the selected BabyB DSL-3 checkpoint, and evaluated both on the official 961 eval rows.

**Commands:** `conda --no-plugins run -n gpu-base python -m babyactionlm.train experiments/configs/v15_babyA_dsl_3.yaml`; `conda --no-plugins run -n gpu-base python -m babyactionlm.evaluate experiments/configs/evaluate_v15_babyA_dsl_3.yaml`; `conda --no-plugins run -n gpu-base python -m babyactionlm.evaluate experiments/configs/evaluate_v15_babyB_dsl_3.yaml`

**Result:** BabyA v1.5 official metrics: parse `0.3632`, function `0.0`, argument exact `0.0937`, exact `0.0`. BabyB v1.5 official metrics: parse `0.1145`, function `0.0083`, argument exact `0.0250`, exact `0.0073`.

**Consequence:** v1.5 produced a small nonzero exact-match result for BabyB, but v1 JSON remains better for BabyB parse and function accuracy.

## 2026-04-29: v1.5 Analysis Artifacts

**Action:** Rebuilt combined tables, plots, qualitative examples, and training curves after v1.5.

**Commands:** `conda --no-plugins run -n gpu-base python -m babyactionlm.training_history`; `conda --no-plugins run -n gpu-base python -m babyactionlm.analysis`

**Result:** Updated `results/summary.csv`, `results/per_tool.csv`, `results/v15_trials.csv`, `results/figures/metric_comparison.png`, `results/figures/per_tool_exact_match.png`, `results/figures/training_curves.png`, and `results/qualitative_examples.md`.

**Consequence:** Report artifacts now compare v1, v1.5, and FunctionGemma.

## 2026-06-12: ACL Report Preparation

**Action:** Checked the current project evidence files and official ACL style/formatting guidance, then added `docs/acl_report_handoff.md`.

**Sources checked:** `results/summary.csv`, `results/v15_trials.csv`, `results/qualitative_examples.md`, `docs/report_draft.md`, `docs/project_memory.md`, https://github.com/acl-org/acl-style-files, and https://acl-org.github.io/ACLPUB/formatting.html.

**Result:** The repo now has a report-writing handoff that records format constraints, supported claims, recommended figures/tables, current metrics, and a prompt for the next chat.

**Consequence:** The next session can start drafting the ACL-style report without rediscovering the experiment state.

## 2026-06-12: Modular ACL Report Draft

**Action:** Created the first modular ACL-style LaTeX report draft from the tracked result artifacts and handoff notes.

**Files created:** `report_outline.md`, `main.tex`, `sections/00_abstract.tex`, `sections/01_introduction.tex`, `sections/02_background.tex`, `sections/03_task_dataset.tex`, `sections/04_models_method.tex`, `sections/05_experiments.tex`, `sections/06_results_analysis.tex`, `sections/07_limitations_conclusion.tex`, `references/references.bib`, `acl.sty`, and `acl_natbib.bst`.

**Result:** Copied report figures into `figures/` and referenced them as `figures/metric_comparison.png` and `figures/training_curves.png`. Static checks confirmed the modular paths and ASCII-only report source. Local PDF compilation was not run because `pdflatex` and `bibtex` are not installed on PATH in this environment.

**Consequence:** The report folder layout is ready for Overleaf or another LaTeX environment with the official ACL style files included.

## 2026-06-12: Report Cohesion Revision

**Action:** Revised the ACL report draft to avoid exposing internal `v1`/`v1.5` experiment labels in the paper prose.

**Files changed:** `sections/00_abstract.tex`, `sections/01_introduction.tex`, `sections/02_background.tex`, `sections/03_task_dataset.tex`, `sections/04_models_method.tex`, `sections/05_experiments.tex`, `sections/06_results_analysis.tex`, `sections/07_limitations_conclusion.tex`, and `report_outline.md`.

**Result:** The report now describes the experiments as compact JSON targets and a DSL format diagnostic, expands domain-specific language once in the abstract, clarifies the GPT-wee citation, and shortens the qualitative table to avoid JSON overflow in the ACL column layout.

**Consequence:** The report should read more cohesively as one experiment while preserving the original results and claim boundaries.

## 2026-09-03: Final Report And Repository Review

**Action:** Audited the final PDF, LaTeX source, code, configs, tests, and curated results before the professor-facing push.

**Verification:** Rendered all four PDF pages for visual inspection; checked report claims against source/config/result files; ran `conda --no-plugins run -n gpu-base pytest -q`.

**Result:** The PDF rendered without clipping, overlap, broken figures, or unreadable text. All 33 tests passed. The headline values in the report match `results/summary.csv`, and the model-selection values match `results/v15_trials.csv`.

**Cleanup:** Updated the README, matched the LaTeX author name to the final PDF, ignored OS/LaTeX temporary files, and excluded redundant report outline, summary, and chat-handoff notes. The final PDF was not modified.

**Consequence:** The existing `babyactionlm-core` repository is the canonical professor-facing project repository.
