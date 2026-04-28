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
