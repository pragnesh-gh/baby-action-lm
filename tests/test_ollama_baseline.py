from babyactionlm.ollama_baseline import normalize_ollama_message, normalize_tools_for_ollama


def test_normalize_ollama_message_prefers_native_tool_call():
    parsed = normalize_ollama_message(
        {
            "message": {
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "show_map",
                            "arguments": {"query": "Berlin"},
                        }
                    }
                ],
            }
        }
    )

    assert parsed.name == "show_map"
    assert parsed.arguments == {"query": "Berlin"}


def test_normalize_ollama_message_falls_back_to_content_json():
    parsed = normalize_ollama_message(
        {"message": {"content": '{"name":"turn_on_flashlight","arguments":{}}'}}
    )

    assert parsed.name == "turn_on_flashlight"
    assert parsed.arguments == {}


def test_normalize_ollama_message_handles_pydantic_style_tool_call_objects():
    class Function:
        name = "show_map"
        arguments = {"query": "Berlin"}

    class ToolCall:
        function = Function()

    class Message:
        content = ""
        tool_calls = [ToolCall()]

    class Response:
        message = Message()

    parsed = normalize_ollama_message(Response())

    assert parsed.name == "show_map"
    assert parsed.arguments == {"query": "Berlin"}


def test_normalize_tools_for_ollama_lowercases_object_and_drops_null_properties():
    tools = normalize_tools_for_ollama(
        [
            {
                "function": {
                    "name": "show_map",
                    "description": "Shows a location.",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {"query": {"type": "STRING"}, "body": None},
                        "required": ["query"],
                    },
                }
            }
        ]
    )

    assert tools == [
        {
            "type": "function",
            "function": {
                "name": "show_map",
                "description": "Shows a location.",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            },
        }
    ]
