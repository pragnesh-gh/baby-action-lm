# Agent Instructions For BabyActionLM

This file is the required entrypoint for every agent working in this repository.

## Start Here

Before making changes, read these files in order:

1. `AGENTS.md`
2. `docs/project_memory.md`
3. `docs/decision_log.md`
4. `docs/assumptions.md`
5. `docs/run_log.md`
6. The active implementation plan in `docs/superpowers/plans/`

If any of these files disagree, stop and update the living docs before continuing.

## Project Thesis

BabyActionLM studies whether BabyLM-scale language models can act as local mobile tool-call controllers. The project is an NLP experiment on simulated phone action parsing, not an Android app.

The core research question is:

Can BabyLM-style pretraining help a very small neural language model learn reliable mobile action parsing?

## Required Superpowers Workflow

Use relevant Superpowers skills before work:

- Use brainstorming/planning skills before changing project scope or experiment design.
- Use executing-plans or subagent-driven-development when implementing a written plan.
- Use systematic-debugging before fixing broken behavior or failed runs.
- Use verification-before-completion before claiming anything is complete, passing, or pushed.

If a Superpowers skill conflicts with this file, follow the user request first, then this file, then the skill.

## Living Documentation Rules

Keep these docs current:

- `docs/project_memory.md`: update after code, config, repo, stage, or project-state changes.
- `docs/decision_log.md`: append after research/design/implementation decisions.
- `docs/assumptions.md`: update when assumptions are added, confirmed, changed, or falsified.
- `docs/run_log.md`: append after dataset inspections, dependency installs, training runs, evaluations, pushes, and verification commands that matter.

Every final response must say whether these docs were updated, or why no doc update was needed.

## Scope Boundaries

In scope:

- Mobile Actions language-to-tool-call parsing.
- BabyA/B fine-tuning and evaluation.
- A scratch tiny model only after BabyA/B pipeline works.
- `functiongemma:270m` as a zero-shot Ollama baseline.
- Small tracked result summaries, plots, and report drafts.

Out of scope:

- Android app development.
- Real execution of phone actions.
- Private phone data collection.
- Training large models.
- Committing model weights, checkpoints, raw datasets, raw logs, or generated caches.

## Artifact Rules

Do not commit:

- `data/`
- `datasets/`
- `models/`
- `checkpoints/`
- `outputs/`
- `runs/`
- `logs/`
- raw prediction dumps
- model weights such as `.safetensors`, `.bin`, `.pt`, `.pth`, `.gguf`

Do commit:

- source code
- tests
- configs
- documentation
- small summary CSVs
- small figures used in the report

## Handoff Checklist

Before handing off to another session:

1. Run `git status --short --branch`.
2. Check that `docs/project_memory.md` reflects the current stage.
3. Check that new decisions are in `docs/decision_log.md`.
4. Check that experiment or verification commands are in `docs/run_log.md`.
5. Push committed documentation or code changes when appropriate.

