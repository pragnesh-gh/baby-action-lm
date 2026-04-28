from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ToolCall:
    name: str | None
    arguments: dict[str, Any]
    raw: Any = None
    parse_error: str | None = None

    @property
    def parsed(self) -> bool:
        return self.parse_error is None and self.name is not None


def _json_ready(value: Any) -> Any:
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _json_ready(inner) for key, inner in value.items() if inner is not None}
    if isinstance(value, list):
        return [_json_ready(item) for item in value if item is not None]
    return value


def clean_arguments(arguments: Any) -> dict[str, Any]:
    if arguments is None:
        return {}
    if isinstance(arguments, str):
        arguments = json.loads(arguments)
    if not isinstance(arguments, Mapping):
        raise TypeError("tool-call arguments must be an object")
    return {
        str(key): _json_ready(value)
        for key, value in arguments.items()
        if value is not None
    }


def _load_first_json_object(text: str) -> Any:
    decoder = json.JSONDecoder()
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object found")
    loaded, _ = decoder.raw_decode(text[start:])
    return loaded


def parse_tool_call(output: str | Mapping[str, Any]) -> ToolCall:
    try:
        loaded: Any = _load_first_json_object(output) if isinstance(output, str) else dict(output)
        if "function" in loaded and isinstance(loaded["function"], Mapping):
            loaded = loaded["function"]
        name = loaded.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("missing string tool name")
        return ToolCall(
            name=name,
            arguments=clean_arguments(loaded.get("arguments", {})),
            raw=output,
            parse_error=None,
        )
    except Exception as exc:
        return ToolCall(name=None, arguments={}, raw=output, parse_error=str(exc))


def from_dataset_function(function: Mapping[str, Any]) -> ToolCall:
    return parse_tool_call(
        {
            "name": function.get("name"),
            "arguments": clean_arguments(function.get("arguments", {})),
        }
    )

