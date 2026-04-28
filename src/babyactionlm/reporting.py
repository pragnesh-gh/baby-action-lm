from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


SUMMARY_COLUMNS = [
    "model",
    "checkpoint",
    "eval_set",
    "n",
    "parse_rate",
    "function_accuracy",
    "argument_exact_match",
    "tool_call_exact_match",
    "timestamp",
    "config_path",
]

PER_TOOL_COLUMNS = [
    "model",
    "eval_set",
    "tool",
    "n",
    "parse_rate",
    "function_accuracy",
    "argument_exact_match",
    "tool_call_exact_match",
]


def _write_csv(path: str | Path, rows: Iterable[dict[str, object]], columns: list[str]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_summary_csv(path: str | Path, rows: Iterable[dict[str, object]]) -> None:
    _write_csv(path, rows, SUMMARY_COLUMNS)


def write_per_tool_csv(path: str | Path, rows: Iterable[dict[str, object]]) -> None:
    _write_csv(path, rows, PER_TOOL_COLUMNS)
