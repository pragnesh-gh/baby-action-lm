from datetime import datetime

from babyactionlm.data import MobileActionRecord
from babyactionlm.formatting import format_example, format_target, tool_signature


def _record():
    return MobileActionRecord(
        id="mobile-actions-000001",
        split="train",
        tools=[
            {
                "function": {
                    "name": "create_calendar_event",
                    "parameters": {
                        "properties": {"title": {"type": "STRING"}, "datetime": {"type": "STRING"}, "body": None},
                        "required": ["title", "datetime"],
                    },
                }
            }
        ],
        messages=[
            {"role": "developer", "content": "Current date: 2026-04-28"},
            {"role": "user", "content": "Schedule project review tomorrow at 10:30."},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "function": {
                            "name": "create_calendar_event",
                            "arguments": {
                                "title": "Project Review",
                                "datetime": datetime(2026, 4, 29, 10, 30),
                                "body": None,
                            },
                        }
                    }
                ],
            },
        ],
    )


def test_tool_signature_uses_only_available_non_null_parameters():
    assert tool_signature(_record().tools[0]) == "create_calendar_event(title,datetime)"


def test_format_target_outputs_compact_canonical_json():
    assert format_target(_record()) == (
        '{"name":"create_calendar_event","arguments":'
        '{"title":"Project Review","datetime":"2026-04-29T10:30:00"}}'
    )


def test_format_example_uses_compact_prompt_and_target():
    example = format_example(_record())

    assert "Tools: create_calendar_event(title,datetime)" in example.prompt
    assert "Command: Schedule project review tomorrow at 10:30." in example.prompt
    assert example.prompt.endswith("JSON:")
    assert example.target.startswith('{"name":"create_calendar_event"')

