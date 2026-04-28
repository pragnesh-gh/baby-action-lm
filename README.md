# BabyActionLM

BabyActionLM is a course project for **Neural Networks for NLP**. The project asks whether a BabyLM-scale language model can act as a tiny local controller for mobile agents by translating natural-language phone commands into structured function calls.

## Research Question

Can BabyLM-style pretraining help a very small neural language model learn reliable mobile action parsing?

We compare:

- a scratch tiny LLaMA-style model, if time allows
- existing BabyA/B tiny BabyLM checkpoints from the course work
- `functiongemma:270m` through Ollama as a modern edge function-calling baseline

## Task

The model receives a user command such as:

```text
Turn on the flashlight.
```

and should emit a structured tool call such as:

```json
{"name":"turn_on_flashlight","arguments":{}}
```

The phone actions are simulated with the `google/mobile-actions` dataset rather than executed on a real Android device.

## Repository Layout

- `docs/` - teacher pitch, scope, and project planning notes
- `src/` - future data preparation, training, and evaluation scripts
- `experiments/` - configs and small experiment summaries
- `results/` - small result tables and figures only
- `notebooks/` - optional exploratory notebooks
- `references/` - paper notes and bibliography material
- `scripts/` - utility commands for local workflow
- `tests/` - future parser/evaluation tests

## Quickstart

1. Create and activate a Python environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Pull the FunctionGemma baseline when ready:

```powershell
ollama pull functiongemma:270m
```

4. Read the teacher-facing pitch:

```powershell
Get-Content docs\pitch_and_plan.md
```

## Important Scope Boundary

This project does **not** build an Android app. It studies the NLP core of a possible on-device agent: mapping language commands to structured phone tool calls.

