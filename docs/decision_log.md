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

