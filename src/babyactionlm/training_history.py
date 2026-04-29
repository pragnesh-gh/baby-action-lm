from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable


def extract_trainer_history(model_name: str, trainer_state_path: str | Path) -> list[dict[str, object]]:
    state = json.loads(Path(trainer_state_path).read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    for entry in state.get("log_history", []):
        if "loss" in entry:
            rows.append(
                {
                    "model": model_name,
                    "step": int(entry["step"]),
                    "epoch": float(entry["epoch"]),
                    "metric": "train_loss",
                    "value": float(entry["loss"]),
                }
            )
        if "eval_loss" in entry:
            rows.append(
                {
                    "model": model_name,
                    "step": int(entry["step"]),
                    "epoch": float(entry["epoch"]),
                    "metric": "eval_loss",
                    "value": float(entry["eval_loss"]),
                }
            )
    return rows


def write_training_history_csv(path: str | Path, rows: Iterable[dict[str, object]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["model", "step", "epoch", "metric", "value"])
        writer.writeheader()
        writer.writerows(rows)


def write_training_curve_plot(rows: list[dict[str, object]], output_path: str | Path) -> None:
    import matplotlib.pyplot as plt

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=False)
    for axis, metric in zip(axes, ["train_loss", "eval_loss"]):
        for model in sorted({str(row["model"]) for row in rows}):
            model_rows = [row for row in rows if row["model"] == model and row["metric"] == metric]
            model_rows.sort(key=lambda row: float(row["epoch"]))
            axis.plot(
                [float(row["epoch"]) for row in model_rows],
                [float(row["value"]) for row in model_rows],
                marker="o" if metric == "eval_loss" else None,
                label=model,
            )
        axis.set_title(metric.replace("_", " ").title())
        axis.set_xlabel("Epoch")
        axis.set_ylabel("Loss")
        axis.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def build_training_history(model_state_paths: dict[str, str | Path], output_csv: str | Path, output_plot: str | Path) -> None:
    rows: list[dict[str, object]] = []
    for model_name, state_path in model_state_paths.items():
        rows.extend(extract_trainer_history(model_name, state_path))
    write_training_history_csv(output_csv, rows)
    write_training_curve_plot(rows, output_plot)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract BabyA/B trainer-state loss curves.")
    parser.add_argument(
        "--state",
        action="append",
        metavar="MODEL=PATH",
        help="Trainer state to include. Can be repeated. Defaults to v1 BabyA/B and selected v1.5 BabyA/B.",
    )
    parser.add_argument("--output-csv", default="results/training_history.csv")
    parser.add_argument("--output-plot", default="results/figures/training_curves.png")
    args = parser.parse_args()
    state_items = args.state or [
        "babyA-v1=outputs/models/babyA/checkpoint-816/trainer_state.json",
        "babyB-v1=outputs/models/babyB/checkpoint-816/trainer_state.json",
        "babyA-v15-dsl-3=outputs/models/v15/babyA-dsl-3/checkpoint-675/trainer_state.json",
        "babyB-v15-dsl-3=outputs/models/v15/babyB-dsl-3/checkpoint-675/trainer_state.json",
    ]
    model_state_paths = {}
    for item in state_items:
        if "=" not in item:
            raise ValueError(f"state must use MODEL=PATH format: {item}")
        model, state_path = item.split("=", 1)
        model_state_paths[model] = state_path
    build_training_history(model_state_paths, args.output_csv, args.output_plot)


if __name__ == "__main__":
    main()
