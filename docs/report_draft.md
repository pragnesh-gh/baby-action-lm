# BabyActionLM Report Draft

## Current Status

The implementation supports the core experimental pipeline: Mobile Actions records can be loaded, formatted into compact BabyLM prompts and JSON tool-call targets, parsed back into canonical tool calls, scored with shared metrics, and written to report-ready CSV files.

Full v1 experiments have now been run on all 961 eval examples.

## Result Table

| Model | Parse Rate | Function Accuracy | Argument Exact Match | Exact Tool-Call Match |
| --- | ---: | ---: | ---: | ---: |
| BabyA | 0.0187 | 0.0031 | 0.0000 | 0.0000 |
| BabyB | 0.3559 | 0.0531 | 0.0000 | 0.0000 |
| FunctionGemma 270M | 0.9813 | 0.7097 | 0.5099 | 0.4964 |

Supporting files:

- `results/summary.csv`
- `results/per_tool.csv`
- `results/figures/metric_comparison.png`
- `results/figures/per_tool_exact_match.png`
- `results/qualitative_examples.md`

## Interpretation Frame

BabyA and BabyB test the BabyLM pretraining question. FunctionGemma is a practical edge function-calling reference point, not a same-size baseline. The project remains a simulated NLP tool-call parsing experiment rather than an Android app.

The current v1 result is mixed but useful. BabyB is much stronger than BabyA on parseability and function accuracy, suggesting that the larger BabyLM pretraining setup helps. However, both Baby models fail exact tool-call matching under the current compact JSON format. This means the honest conclusion is not that BabyB is already a reliable phone controller. The stronger claim is that BabyLM-style pretraining gives a measurable advantage, but v1 formatting/training is not sufficient for reliable structured action control.

FunctionGemma provides the practical baseline: it is far better at native tool calling, with about 0.50 exact tool-call match on the same eval split. This makes the project more credible because it shows the task is measurable and nontrivial, not because BabyA/B are expected to beat a specialized 270M function-calling model.

## Next Interpretation Question

For the final report, decide whether to keep v1 as the main result or run v1.5. v1.5 would try to improve BabyA/B parseability with a more constrained target format or prompt, while keeping the same eval split and metrics.
