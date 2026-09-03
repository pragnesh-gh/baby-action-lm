# Decision Log

This file is append-only except for typo fixes.

## 2026-04-28: Project Direction

**Decision:** Build BabyActionLM around mobile tool-call parsing rather than dialogue generation.

**Reason:** The mobile-agent idea is current, scoped, and concrete. It keeps the project tied to language data and neural models while avoiding a too-large Android app or general chatbot.

**Alternatives considered:** Dialogue generation from media transcripts; BabyA/B BLiMP-only analysis.

**Consequences:** The project uses Mobile Actions and function-calling metrics instead of human dialogue evaluation.

## 2026-04-28: Core Thesis

**Decision:** Test whether BabyLM-style pretraining helps tiny models become local phone action parsers.

**Reason:** This gives a scientific question: compare BabyA and BabyB after the same task fine-tuning, and compare them with a modern function-calling baseline.

**Alternatives considered:** Train only one tiny parser; focus only on FunctionGemma; build a real phone app.

**Consequences:** The project remains an NLP experiment and does not require Android integration.

## 2026-04-28: Dataset

**Decision:** Use `google/mobile-actions`.

**Reason:** It directly matches the target task: natural-language mobile commands mapped to structured function calls.

**Alternatives considered:** Create a synthetic dataset manually; scrape or collect phone commands.

**Consequences:** The implementation must split rows by `metadata` because Hugging Face exposes the dataset as one `train` split.

## 2026-04-28: Baseline

**Decision:** Use `functiongemma:270m` through Ollama as a zero-shot baseline.

**Reason:** It is a modern edge function-calling model and is small enough to run locally.

**Alternatives considered:** Fine-tune FunctionGemma; use local 2B/4B models; skip the modern baseline.

**Consequences:** FunctionGemma is treated as a reference point, not the main model to beat.

## 2026-04-28: Living Documentation

**Decision:** Add `AGENTS.md` and living docs before dataset download or model code.

**Reason:** Future sessions should resume without the user repeating context, decisions, assumptions, and current state.

**Alternatives considered:** Keep all context in chat only; rely only on README and pitch docs.

**Consequences:** Agents must update project memory, decision log, assumptions, and run log after meaningful changes.

## 2026-04-28: Canonical Checkpoint Paths

**Decision:** Use nested BabyA/B artifacts under `../Assignments/Main/models/babyA/final/final` and `../Assignments/Main/models/babyB/final/final`.

**Reason:** The nested artifacts have consistent tokenizer/model settings: `pad_token_id=1`, vocab size 8000, and 128-token context.

**Alternatives considered:** Use the parent `final` folders.

**Consequences:** Experiment configs point to the nested `final/final` directories.

## 2026-04-28: Prompt And Target Contract

**Decision:** Fine-tune BabyA/B on a compact prompt and compact canonical JSON target.

**Reason:** BabyA/B have a 128-token context window, so verbose tool descriptions risk crowding out the command and target.

**Alternatives considered:** Include full developer context and full tool descriptions.

**Consequences:** The v1 prompt uses tool signatures only, and evaluation left-truncates prompts to leave room for generated JSON.

## 2026-04-28: Metric Contract

**Decision:** Score parse rate, function accuracy, argument exact match, exact tool-call match, and per-tool summaries over all examples.

**Reason:** These metrics directly reflect structured parsing behavior and keep BabyA/B and FunctionGemma comparable.

**Alternatives considered:** Required-argument-only scoring; partial string similarity.

**Consequences:** Extra predicted arguments make argument exact match false; argument key order does not matter.

## 2026-04-28: Smoke-First Training Defaults

**Decision:** Start with full fine-tuning, 128-token examples, `learning_rate=5e-5`, batch size 4, gradient accumulation 8, and one-epoch smoke runs before full 3-epoch BabyA/B runs.

**Reason:** The local GPU has 4 GB VRAM, and smoke runs catch formatting/model issues quickly.

**Alternatives considered:** LoRA; scratch training first; full BabyA/B training immediately.

**Consequences:** `experiments/configs/smoke.yaml`, `babyA.yaml`, and `babyB.yaml` encode conservative defaults.

## 2026-04-28: FunctionGemma Adapter

**Decision:** Use Ollama native tool calling for FunctionGemma and normalize Ollama pydantic tool-call objects into the shared `ToolCall` schema.

**Reason:** Native tool calling is the fair practical baseline for a function-calling model; parsing must handle Ollama's object responses, not only dicts.

**Alternatives considered:** Prompt-only JSON baseline.

**Consequences:** Mobile Actions tool schemas are normalized for Ollama by lowercasing schema types and dropping null properties.

## 2026-04-28: Version Roadmap

**Decision:** Document v1 through v4 in `docs/version_roadmap.md`.

**Reason:** The project should not become confusing after v1. v1 is the course deliverable; v1.5, v2, v3, and v4 are optional strengthening paths.

**Alternatives considered:** Keep only the active implementation plan.

**Consequences:** Future sessions should refer to the roadmap before proposing extra experiments.

## 2026-04-28: Full Evaluation Scope

**Decision:** Use all 961 Mobile Actions eval examples for BabyA, BabyB, and FunctionGemma.

**Reason:** The eval split is below the planned 1000-example cap, and full evaluation gives a stronger comparison than smoke metrics.

**Alternatives considered:** Keep only 32-example smoke results; use a capped subset.

**Consequences:** `results/summary.csv`, `results/per_tool.csv`, figures, and qualitative examples are based on the full eval split by default.

## 2026-04-28: v1 Result Interpretation

**Decision:** Treat the current BabyA/B result as a valid v1 baseline, but consider v1.5 if we want better Baby parseability.

**Reason:** BabyB substantially improves over BabyA in parse rate, but both Baby models still have zero exact tool-call match under the v1 prompt/target format.

**Alternatives considered:** Hide weak Baby results; immediately change the task definition.

**Consequences:** The report should honestly distinguish "pretraining helps parseability" from "the tiny model is not yet a reliable controller."

## 2026-04-29: v1.5 Dev Split

**Decision:** Split `metadata=train` into train/dev for v1.5 selection and reserve the 961 `metadata=eval` rows for final evaluation only.

**Reason:** v1.5 changes prompt/target format and epoch count, so selecting on the official eval split would weaken the scientific protocol.

**Alternatives considered:** Continue using official eval during trial selection; create a random eval subset from all rows.

**Consequences:** v1.5 trial summaries live under `results/v15/`, while final official v1.5 summaries live at top level in `results/`.

## 2026-04-29: v1.5 DSL Target Format

**Decision:** Add `dsl_v1` targets formatted as `tool=tool_name;arg=value`, with percent-escaped values and parsing back into the shared `ToolCall` schema.

**Reason:** BabyA/B may fail exact JSON generation partly because JSON punctuation and nested structure are hard under a 128-token context. A flatter target tests whether formatting is the bottleneck.

**Alternatives considered:** Keep only JSON and train longer; add verbose tool descriptions; switch to a classification head.

**Consequences:** v1.5 remains comparable because all outputs are normalized into the same metrics, but DSL parse/function behavior is not identical to JSON behavior.

## 2026-04-29: v1.5 Trial Selection

**Decision:** Select `babyB-v15-dsl-3` as the v1.5 setup.

**Reason:** It was the only BabyB dev trial with nonzero exact tool-call match: exact `0.0080`, argument exact `0.0172`, parse `0.1068`, function `0.0115`.

**Alternatives considered:** `json_v1` 3 epochs, `json_v1` 8 epochs, and `dsl_v1` 8 epochs. JSON-8 had better parse/function scores but still zero exact match; DSL-8 lost the exact-match signal.

**Consequences:** Final v1.5 official eval uses DSL-3 for BabyA and BabyB. The report should present v1.5 as a diagnostic strengthening, not as a clean improvement over v1.

## 2026-06-12: ACL Report Handoff

**Decision:** Prepare the final write-up as an approximately 5-page ACL-style double-column report and use `docs/acl_report_handoff.md` as the report-writing entrypoint.

**Reason:** Sina approved the implementation as enough for a project and specifically recommended the ACL style files and typical ACL paper structure.

**Alternatives considered:** Keep using the one-page Markdown report summary; write a free-form university report without ACL formatting.

**Consequences:** The report should prioritize a compact ACL-like structure, a main result table, metric and training-curve figures, one qualitative example, and honest limitations instead of adding new experiments by default.

## 2026-06-12: Modular ACL Report Layout

**Decision:** Store the final report as root-level `main.tex`, section files in `sections/`, imported report figures in `figures/`, and BibTeX entries in `references/references.bib`.

**Reason:** This matches the requested import-friendly layout and makes it easy to revise individual paper sections independently.

**Alternatives considered:** Keep a single monolithic `.tex` file; place the report under a nested `report/` directory.

**Consequences:** Figure paths in the paper use `figures/...`, section paths use `sections/...`, and bibliography paths use `references/...`.

## 2026-09-03: Professor-Facing Repository

**Decision:** Publish the final report and its source in the existing `babyactionlm-core` repository rather than creating a duplicate repository.

**Reason:** The existing repository contains the experiment history, implementation, tests, configs, and curated results that support the report.

**Alternatives considered:** Create a separate clean repository; publish only the PDF; substantially rewrite the implementation after the report was finalized.

**Consequences:** The final PDF remains unchanged, the implementation that produced the reported artifacts is preserved, the README is updated for a professor, and temporary report-planning/chat-handoff files are excluded.

## 2026-09-03: Include Base-Model Provenance

**Decision:** Copy the BabyA/B pretraining notebooks and corpus normalization script from the earlier model-development work into `pretraining/`, with notebook outputs removed and a concise provenance manifest.

**Reason:** The downstream project depends on the BabyA/B base checkpoints, and a professor reviewing only this public repository should be able to inspect how those models were created.

**Alternatives considered:** Require access to a second private repository; duplicate all model checkpoints and corpora; leave the base models undocumented.

**Consequences:** Pretraining source, architecture settings, and Gutenberg source IDs are visible in one repository. Generated weights and data remain excluded according to the artifact policy.
