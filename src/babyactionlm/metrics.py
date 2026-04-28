from __future__ import annotations

from collections import defaultdict
from typing import Sequence

from babyactionlm.schema import ToolCall


def _rate(count: int, total: int) -> float:
    return count / total if total else 0.0


def _counts(golds: Sequence[ToolCall], preds: Sequence[ToolCall]) -> dict[str, int]:
    if len(golds) != len(preds):
        raise ValueError("gold and prediction counts must match")
    parsed = function_correct = arguments_correct = exact = 0
    for gold, pred in zip(golds, preds):
        if pred.parsed:
            parsed += 1
        same_name = pred.parsed and pred.name == gold.name
        same_args = pred.parsed and pred.arguments == gold.arguments
        if same_name:
            function_correct += 1
        if same_args:
            arguments_correct += 1
        if same_name and same_args:
            exact += 1
    return {
        "n": len(golds),
        "parsed": parsed,
        "function_correct": function_correct,
        "arguments_correct": arguments_correct,
        "exact": exact,
    }


def score_predictions(
    golds: Sequence[ToolCall],
    preds: Sequence[ToolCall],
    *,
    model: str,
    eval_set: str,
    checkpoint: str = "",
    timestamp: str = "",
    config_path: str = "",
) -> dict[str, object]:
    counts = _counts(golds, preds)
    total = counts["n"]
    return {
        "model": model,
        "checkpoint": checkpoint,
        "eval_set": eval_set,
        "n": total,
        "parse_rate": _rate(counts["parsed"], total),
        "function_accuracy": _rate(counts["function_correct"], total),
        "argument_exact_match": _rate(counts["arguments_correct"], total),
        "tool_call_exact_match": _rate(counts["exact"], total),
        "timestamp": timestamp,
        "config_path": config_path,
    }


def per_tool_summary(
    golds: Sequence[ToolCall],
    preds: Sequence[ToolCall],
    *,
    model: str,
    eval_set: str,
) -> list[dict[str, object]]:
    grouped: dict[str, list[tuple[ToolCall, ToolCall]]] = defaultdict(list)
    for gold, pred in zip(golds, preds):
        grouped[str(gold.name)].append((gold, pred))

    rows: list[dict[str, object]] = []
    for tool in sorted(grouped):
        pairs = grouped[tool]
        tool_golds = [gold for gold, _ in pairs]
        tool_preds = [pred for _, pred in pairs]
        row = score_predictions(tool_golds, tool_preds, model=model, eval_set=eval_set)
        rows.append(
            {
                "model": row["model"],
                "eval_set": row["eval_set"],
                "tool": tool,
                "n": row["n"],
                "parse_rate": row["parse_rate"],
                "function_accuracy": row["function_accuracy"],
                "argument_exact_match": row["argument_exact_match"],
                "tool_call_exact_match": row["tool_call_exact_match"],
            }
        )
    return rows

