# BabyActionLM

BabyActionLM is a Neural Networks for NLP course project about mobile tool-call parsing with very small language models. It tests whether the course BabyA and BabyB checkpoints can map natural-language phone commands to structured function calls.

The project is a simulated NLP experiment. It does not execute actions on an Android device.

## Final report

The submitted ACL-style report is available at [BabyActionLM_ProjectReport.pdf](BabyActionLM_ProjectReport.pdf). Its LaTeX source is included in `main.tex`, `sections/`, and `references/`.

## Experiment

- Dataset: `google/mobile-actions`
- Official metadata split: 8,693 training rows and 961 evaluation rows
- Models: course BabyA and BabyB checkpoints
- Reference baseline: zero-shot `functiongemma:270m` through Ollama native tool calling
- Targets: compact JSON, plus a flatter DSL diagnostic
- Metrics: parse rate, function accuracy, argument exact match, and complete tool-call exact match

### Reported evaluation results

| Model | Parse rate | Function accuracy | Argument exact match | Tool-call exact match |
| --- | ---: | ---: | ---: | ---: |
| BabyA JSON | 0.0187 | 0.0031 | 0.0000 | 0.0000 |
| BabyB JSON | 0.3559 | 0.0531 | 0.0000 | 0.0000 |
| FunctionGemma 270M | 0.9813 | 0.7097 | 0.5099 | 0.4964 |
| BabyA DSL | 0.3632 | 0.0000 | 0.0937 | 0.0000 |
| BabyB DSL | 0.1145 | 0.0083 | 0.0250 | 0.0073 |

The main finding is modest: BabyB produces more parseable outputs and more correct function names than BabyA under the JSON setup, but neither Baby model is reliable enough to act as a phone controller. FunctionGemma is substantially stronger.

## Repository layout

- `src/babyactionlm/` - dataset, formatting, training, evaluation, baseline, and analysis code
- `tests/` - unit tests for the core pipeline
- `experiments/configs/` - configurations used for training and evaluation
- `results/` - curated summary CSVs, figures, and qualitative examples
- `main.tex`, `sections/`, `references/` - report source
- `docs/` - project scope, experiment decisions, and run history

Raw datasets, model checkpoints, raw predictions, and generated caches are intentionally excluded from Git. The BabyA/B base checkpoints are course artifacts stored outside this repository.

## Setup

The experiments were run with Python 3.11 in a Conda environment named `gpu-base`.

```powershell
conda --no-plugins run -n gpu-base python -m pip install -r requirements.txt
conda --no-plugins run -n gpu-base python -m pip install -e .
conda --no-plugins run -n gpu-base pytest -q
```

The checkpoint paths in `experiments/configs/` may need to be adjusted to match the local location of the course BabyA/B artifacts.

## Main commands

```powershell
# Fine-tune BabyA and BabyB
conda --no-plugins run -n gpu-base python -m babyactionlm.train experiments/configs/babyA.yaml
conda --no-plugins run -n gpu-base python -m babyactionlm.train experiments/configs/babyB.yaml

# Evaluate the fine-tuned checkpoints
conda --no-plugins run -n gpu-base python -m babyactionlm.evaluate experiments/configs/evaluate_babyA.yaml
conda --no-plugins run -n gpu-base python -m babyactionlm.evaluate experiments/configs/evaluate_babyB.yaml

# Run the FunctionGemma reference baseline
ollama pull functiongemma:270m
conda --no-plugins run -n gpu-base python -m babyactionlm.ollama_baseline experiments/configs/functiongemma_zero_shot.yaml

# Rebuild curated tables and plots
conda --no-plugins run -n gpu-base python -m babyactionlm.analysis
```
