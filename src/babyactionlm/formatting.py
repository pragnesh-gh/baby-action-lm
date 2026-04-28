from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from babyactionlm.data import MobileActionRecord
from babyactionlm.schema import from_dataset_function


@dataclass(frozen=True)
class FormattedExample:
    id: str
    split: str
    prompt: str
    target: str


def tool_signature(tool: dict[str, Any]) -> str:
    function = tool["function"]
    parameters = function.get("parameters") or {}
    properties = parameters.get("properties") or {}
    argument_names = [name for name, spec in properties.items() if spec is not None]
    return f"{function['name']}({','.join(argument_names)})"


def extract_user_command(record: MobileActionRecord) -> str:
    return str(record.messages[1]["content"])


def extract_gold_function(record: MobileActionRecord) -> dict[str, Any]:
    return dict(record.messages[2]["tool_calls"][0]["function"])


def format_target(record: MobileActionRecord) -> str:
    tool_call = from_dataset_function(extract_gold_function(record))
    return json.dumps(
        {"name": tool_call.name, "arguments": tool_call.arguments},
        ensure_ascii=False,
        separators=(",", ":"),
    )


def format_prompt(record: MobileActionRecord) -> str:
    tools = "; ".join(tool_signature(tool) for tool in record.tools)
    return "\n".join(
        [
            "Task: map the command to one mobile tool call.",
            f"Tools: {tools}",
            f"Command: {extract_user_command(record)}",
            "JSON:",
        ]
    )


def format_example(record: MobileActionRecord) -> FormattedExample:
    return FormattedExample(
        id=record.id,
        split=record.split,
        prompt=format_prompt(record),
        target=format_target(record),
    )

