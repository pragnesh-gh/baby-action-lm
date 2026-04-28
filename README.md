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
- `src/` - data preparation, formatting, training, evaluation, and baseline scripts
- `experiments/` - YAML configs and small experiment summaries
- `results/` - small result tables and figures only
- `notebooks/` - optional exploratory notebooks
- `references/` - paper notes and bibliography material
- `tests/` - parser, formatting, metric, training, and baseline tests

## Quickstart

The current local execution target is the existing Conda environment `gpu-base`.

1. Install the package and dependencies:

```powershell
conda --no-plugins run -n gpu-base python -m pip install -r requirements.txt
conda --no-plugins run -n gpu-base python -m pip install -e .
```

2. Run tests:

```powershell
conda --no-plugins run -n gpu-base pytest -q
```

3. Run the BabyB smoke fine-tune:

```powershell
conda --no-plugins run -n gpu-base python -m babyactionlm.train experiments/configs/smoke.yaml
```

4. Evaluate the BabyB smoke checkpoint:

```powershell
conda --no-plugins run -n gpu-base python -m babyactionlm.evaluate experiments/configs/evaluate_smoke.yaml
```

5. Pull and run the FunctionGemma smoke baseline:

```powershell
ollama pull functiongemma:270m
conda --no-plugins run -n gpu-base python -m babyactionlm.ollama_baseline experiments/configs/functiongemma_smoke.yaml
```

6. Read the teacher-facing pitch:

```powershell
Get-Content docs\pitch_and_plan.md
```

## Important Scope Boundary

This project does **not** build an Android app. It studies the NLP core of a possible on-device agent: mapping language commands to structured phone tool calls.
