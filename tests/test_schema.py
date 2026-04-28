import json
from datetime import datetime

from babyactionlm.schema import ToolCall, from_dataset_function, parse_tool_call


def test_parse_tool_call_accepts_compact_json():
    parsed = parse_tool_call('{"name":"show_map","arguments":{"query":"Berlin"}}')

    assert parsed == ToolCall(
        name="show_map",
        arguments={"query": "Berlin"},
        raw='{"name":"show_map","arguments":{"query":"Berlin"}}',
        parse_error=None,
    )


def test_parse_tool_call_normalizes_stringified_arguments_and_drops_nulls():
    parsed = parse_tool_call(
        {
            "name": "send_email",
            "arguments": json.dumps({"to": "a@example.com", "subject": "Hi", "body": None}),
        }
    )

    assert parsed.name == "send_email"
    assert parsed.arguments == {"to": "a@example.com", "subject": "Hi"}
    assert parsed.parse_error is None


def test_parse_tool_call_returns_failure_object_for_malformed_output():
    parsed = parse_tool_call("not json")

    assert parsed.name is None
    assert parsed.arguments == {}
    assert parsed.parse_error


def test_from_dataset_function_converts_datetime_and_drops_null_arguments():
    parsed = from_dataset_function(
        {
            "name": "create_calendar_event",
            "arguments": {
                "title": "Project Review",
                "datetime": datetime(2026, 4, 28, 10, 30),
                "body": None,
            },
        }
    )

    assert parsed.name == "create_calendar_event"
    assert parsed.arguments == {
        "title": "Project Review",
        "datetime": "2026-04-28T10:30:00",
    }

