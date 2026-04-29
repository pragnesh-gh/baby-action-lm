# BabyActionLM Report Draft

## Current Status

The implementation supports the core experimental pipeline: Mobile Actions records can be loaded, formatted into compact BabyLM prompts and JSON tool-call targets, parsed back into canonical tool calls, scored with shared metrics, and written to report-ready CSV files.

Full v1 and v1.5 experiments have now been run on all 961 official eval examples.

## Result Table

| Model | Parse Rate | Function Accuracy | Argument Exact Match | Exact Tool-Call Match |
| --- | ---: | ---: | ---: | ---: |
| BabyA | 0.0187 | 0.0031 | 0.0000 | 0.0000 |
| BabyB | 0.3559 | 0.0531 | 0.0000 | 0.0000 |
| FunctionGemma 270M | 0.9813 | 0.7097 | 0.5099 | 0.4964 |
| BabyA v1.5 DSL-3 | 0.3632 | 0.0000 | 0.0937 | 0.0000 |
| BabyB v1.5 DSL-3 | 0.1145 | 0.0083 | 0.0250 | 0.0073 |

Supporting files:

- `results/summary.csv`
- `results/per_tool.csv`
- `results/figures/metric_comparison.png`
- `results/figures/per_tool_exact_match.png`
- `results/figures/training_curves.png`
- `results/v15_trials.csv`
- `results/qualitative_examples.md`

## Interpretation Frame

BabyA and BabyB test the BabyLM pretraining question. FunctionGemma is a practical edge function-calling reference point, not a same-size baseline. The project remains a simulated NLP tool-call parsing experiment rather than an Android app.

The current v1 result is mixed but useful. BabyB is much stronger than BabyA on parseability and function accuracy, suggesting that the larger BabyLM pretraining setup helps. However, both Baby models fail exact tool-call matching under the current compact JSON format. This means the honest conclusion is not that BabyB is already a reliable phone controller. The stronger claim is that BabyLM-style pretraining gives a measurable advantage, but v1 formatting/training is not sufficient for reliable structured action control.

FunctionGemma provides the practical baseline: it is far better at native tool calling, with about 0.50 exact tool-call match on the same eval split. This makes the project more credible because it shows the task is measurable and nontrivial, not because BabyA/B are expected to beat a specialized 270M function-calling model.

## v1.5 Interpretation

v1.5 tested whether the zero exact-match result was mostly a JSON-formatting problem. The protocol used a dev split from the training rows for selection and kept the official eval split untouched until the final run. Four BabyB trials were compared: JSON-3, JSON-8, DSL-3, and DSL-8.

The best dev trial by exact match was DSL-3. On official eval it gave BabyB a small nonzero exact tool-call match of `0.0073`, so the format hypothesis has some support. However, the result is not a general improvement: BabyB v1 JSON still has much better parse rate and function accuracy. The report should therefore say that target format matters, but it does not solve the tiny-controller problem.

BabyA v1.5 is also instructive. It reaches a higher parse rate under DSL, but function accuracy remains `0.0`; many parsed strings are structurally parseable without being semantically correct. This is a useful warning that parse rate alone is not enough.

## Final Report Angle

The most defensible conclusion is:

BabyLM-style pretraining helps tiny models move toward structured action parsing, visible in BabyB's v1 advantage over BabyA and in lower training/eval losses. But under a 128-token context and simple causal-LM fine-tuning, these models are not reliable mobile tool-call controllers. v1.5 shows that output format can create a tiny exact-match signal, while FunctionGemma shows what a practical edge function-calling baseline looks like.
