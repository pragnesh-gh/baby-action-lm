from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from babyactionlm.config import load_yaml
from babyactionlm.data import load_mobile_actions, select_eval_records
from babyactionlm.formatting import extract_user_command
from babyactionlm.metrics import per_tool_summary, score_predictions
from babyactionlm.reporting import write_per_tool_csv, write_summary_csv
from babyactionlm.schema import ToolCall, from_dataset_function, parse_tool_call


def _get_value(item: Any, key: str, default: Any = None) -> Any:
    if isinstance(item, Mapping):
        return item.get(key, default)
    return getattr(item, key, default)


def normalize_ollama_message(response: Mapping[str, Any] | Any) -> ToolCall:
    message = _get_value(response, "message", response)
    tool_calls = _get_value(message, "tool_calls")
    if tool_calls:
        first = tool_calls[0]
        function = _get_value(first, "function", first)
        name = _get_value(function, "name")
        arguments = _get_value(function, "arguments", {})
        if name:
            return parse_tool_call({"name": name, "arguments": arguments})
    content = _get_value(message, "content", "")
    return parse_tool_call(str(content))


def _normalize_schema_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        normalized = {}
        for key, inner in value.items():
            if inner is None:
                continue
            if key == "type" and isinstance(inner, str):
                normalized[key] = inner.lower()
            elif key == "properties" and isinstance(inner, Mapping):
                normalized[key] = {
                    str(name): _normalize_schema_value(spec)
                    for name, spec in inner.items()
                    if spec is not None
                }
            else:
                normalized[key] = _normalize_schema_value(inner)
        return normalized
    if isinstance(value, list):
        return [_normalize_schema_value(item) for item in value]
    return value


def normalize_tools_for_ollama(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized_tools = []
    for tool in tools:
        function = tool["function"]
        parameters = _normalize_schema_value(function.get("parameters") or {"type": "object", "properties": {}})
        normalized_tools.append(
            {
                "type": "function",
                "function": {
                    "name": function["name"],
                    "description": function.get("description", ""),
                    "parameters": parameters,
                },
            }
        )
    return normalized_tools


def _tool_specs(record: Any) -> list[dict[str, Any]]:
    return normalize_tools_for_ollama(list(record.tools))


def _fallback_prompt(record: Any) -> str:
    tool_names = [tool["function"]["name"] for tool in record.tools]
    return (
        "Return only compact JSON with keys name and arguments for one mobile tool call.\n"
        f"Tools: {', '.join(tool_names)}\n"
        f"Command: {extract_user_command(record)}"
    )


def run_ollama_baseline(config_path: str | Path) -> None:
    import ollama

    config = load_yaml(config_path)
    records = select_eval_records(load_mobile_actions(), cap=int(config.get("eval_cap", 1000)), seed=int(config.get("seed", 42)))
    if config.get("eval_limit"):
        records = records[: int(config["eval_limit"])]

    model = str(config.get("model", "functiongemma:270m"))
    use_native_tools = bool(config.get("use_native_tools", True))
    golds = []
    preds = []
    raw_rows = []
    for record in records:
        messages = [{"role": "user", "content": _fallback_prompt(record)}]
        kwargs: dict[str, Any] = {"model": model, "messages": messages, "options": {"temperature": 0}}
        if use_native_tools:
            kwargs["tools"] = _tool_specs(record)
        response = ollama.chat(**kwargs)
        pred = normalize_ollama_message(response)
        gold = from_dataset_function(record.messages[2]["tool_calls"][0]["function"])
        golds.append(gold)
        preds.append(pred)
        raw_rows.append({"id": record.id, "gold": gold.__dict__, "prediction": pred.__dict__, "response": response})

    timestamp = datetime.now().isoformat(timespec="seconds")
    summary = score_predictions(
        golds,
        preds,
        model=model,
        eval_set=str(config.get("eval_set", "eval")),
        checkpoint=model,
        timestamp=timestamp,
        config_path=str(config_path),
    )
    raw_path = Path(config.get("raw_predictions_path", "outputs/predictions/functiongemma_predictions.jsonl"))
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    with raw_path.open("w", encoding="utf-8") as handle:
        for row in raw_rows:
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")

    write_summary_csv(config.get("summary_path", "results/functiongemma_summary.csv"), [summary])
    write_per_tool_csv(
        config.get("per_tool_path", "results/functiongemma_per_tool.csv"),
        per_tool_summary(golds, preds, model=model, eval_set=str(summary["eval_set"])),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate functiongemma:270m with Ollama.")
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    run_ollama_baseline(args.config)


if __name__ == "__main__":
    main()
