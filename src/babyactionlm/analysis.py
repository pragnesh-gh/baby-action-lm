from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable


SUMMARY_GLOB = "*summary.csv"
PER_TOOL_GLOB = "*per-tool.csv"


def combine_csv_files(paths: Iterable[str | Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path_like in paths:
        path = Path(path_like)
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                row["source_file"] = path.name
                rows.append(row)
    return rows


def write_rows(path: str | Path, rows: list[dict[str, object]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        output.write_text("", encoding="utf-8")
        return
    columns = list(rows[0].keys())
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _same_tool_call(row: dict) -> bool:
    gold = row.get("gold", {})
    prediction = row.get("prediction", {})
    return gold.get("name") == prediction.get("name") and gold.get("arguments") == prediction.get("arguments")


def _bucket(row: dict) -> str:
    prediction = row.get("prediction", {})
    if prediction.get("parse_error"):
        return "parse_error"
    if _same_tool_call(row):
        return "correct"
    if row.get("gold", {}).get("name") != prediction.get("name"):
        return "wrong_tool"
    return "wrong_arguments"


def collect_qualitative_examples(paths: Iterable[str | Path], limit_per_bucket: int = 5) -> dict[str, list[dict]]:
    buckets = {"correct": [], "parse_error": [], "wrong_tool": [], "wrong_arguments": []}
    for path_like in paths:
        path = Path(path_like)
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                bucket = _bucket(row)
                if len(buckets[bucket]) < limit_per_bucket:
                    row["source_file"] = path.name
                    buckets[bucket].append(row)
    return buckets


def write_qualitative_markdown(path: str | Path, examples: dict[str, list[dict]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Qualitative Examples", ""]
    for bucket, rows in examples.items():
        lines.extend([f"## {bucket.replace('_', ' ').title()}", ""])
        if not rows:
            lines.extend(["No examples collected.", ""])
            continue
        for row in rows:
            lines.extend(
                [
                    f"- Source: `{row.get('source_file', '')}` / ID: `{row.get('id', '')}`",
                    f"  - Command: {row.get('command', '')}",
                    f"  - Gold: `{json.dumps(row.get('gold', {}), ensure_ascii=False, default=str)}`",
                    f"  - Prediction: `{json.dumps(row.get('prediction', {}), ensure_ascii=False, default=str)}`",
                    "",
                ]
            )
    output.write_text("\n".join(lines), encoding="utf-8")


def write_metric_plot(summary_rows: list[dict[str, str]], output_path: str | Path) -> None:
    import matplotlib.pyplot as plt

    metrics = ["parse_rate", "function_accuracy", "argument_exact_match", "tool_call_exact_match"]
    labels = [row["model"] for row in summary_rows]
    x_positions = range(len(labels))
    width = 0.18
    fig, ax = plt.subplots(figsize=(10, 5))
    for offset, metric in enumerate(metrics):
        values = [float(row.get(metric, 0.0) or 0.0) for row in summary_rows]
        shifted = [x + (offset - 1.5) * width for x in x_positions]
        ax.bar(shifted, values, width=width, label=metric)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    ax.set_title("BabyActionLM Metric Comparison")
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.legend()
    fig.tight_layout()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)


def write_per_tool_plot(per_tool_rows: list[dict[str, str]], output_path: str | Path) -> None:
    import matplotlib.pyplot as plt

    if not per_tool_rows:
        return
    models = sorted({row["model"] for row in per_tool_rows})
    tools = sorted({row["tool"] for row in per_tool_rows})
    lookup = {
        (row["model"], row["tool"]): float(row.get("tool_call_exact_match", 0.0) or 0.0)
        for row in per_tool_rows
    }
    fig, ax = plt.subplots(figsize=(11, 5.5))
    width = 0.8 / max(1, len(models))
    x_positions = range(len(tools))
    for model_index, model in enumerate(models):
        shifted = [x + (model_index - (len(models) - 1) / 2) * width for x in x_positions]
        values = [lookup.get((model, tool), 0.0) for tool in tools]
        ax.bar(shifted, values, width=width, label=model)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Exact Tool-Call Match")
    ax.set_title("Per-Tool Exact Match")
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(tools, rotation=25, ha="right")
    ax.legend()
    fig.tight_layout()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)


def build_analysis(results_dir: str | Path = "results", raw_dir: str | Path = "outputs/predictions") -> None:
    results = Path(results_dir)
    summary_files = sorted(
        path for path in results.glob(SUMMARY_GLOB)
        if path.name != "summary.csv" and "smoke" not in path.name
    )
    per_tool_files = sorted(
        path for path in results.glob(PER_TOOL_GLOB)
        if path.name != "per_tool.csv" and "smoke" not in path.name
    )
    summary_rows = combine_csv_files(summary_files)
    per_tool_rows = combine_csv_files(per_tool_files)
    write_rows(results / "summary.csv", summary_rows)
    write_rows(results / "per_tool.csv", per_tool_rows)
    if summary_rows:
        write_metric_plot(summary_rows, results / "figures" / "metric_comparison.png")
    if per_tool_rows:
        write_per_tool_plot(per_tool_rows, results / "figures" / "per_tool_exact_match.png")
    raw_files = sorted(path for path in Path(raw_dir).glob("*.jsonl") if "smoke" not in path.name)
    examples = collect_qualitative_examples(raw_files)
    write_qualitative_markdown(results / "qualitative_examples.md", examples)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build combined result tables, plots, and qualitative examples.")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--raw-dir", default="outputs/predictions")
    args = parser.parse_args()
    build_analysis(args.results_dir, args.raw_dir)


if __name__ == "__main__":
    main()
