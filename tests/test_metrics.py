from babyactionlm.metrics import per_tool_summary, score_predictions
from babyactionlm.schema import ToolCall


def test_score_predictions_computes_core_rates_over_all_examples():
    golds = [
        ToolCall("show_map", {"query": "Berlin"}),
        ToolCall("send_email", {"to": "a@example.com", "subject": "Hi"}),
        ToolCall("turn_on_flashlight", {}),
    ]
    preds = [
        ToolCall("show_map", {"query": "Berlin"}),
        ToolCall("send_email", {"to": "a@example.com"}),
        ToolCall(None, {}, parse_error="bad json"),
    ]

    scores = score_predictions(golds, preds, model="babyB", eval_set="smoke")

    assert scores["model"] == "babyB"
    assert scores["eval_set"] == "smoke"
    assert scores["n"] == 3
    assert scores["parse_rate"] == 2 / 3
    assert scores["function_accuracy"] == 2 / 3
    assert scores["argument_exact_match"] == 1 / 3
    assert scores["tool_call_exact_match"] == 1 / 3


def test_per_tool_summary_groups_by_gold_tool():
    golds = [
        ToolCall("show_map", {"query": "Berlin"}),
        ToolCall("show_map", {"query": "Paris"}),
        ToolCall("send_email", {"to": "a@example.com", "subject": "Hi"}),
    ]
    preds = [
        ToolCall("show_map", {"query": "Berlin"}),
        ToolCall("show_map", {"query": "Lyon"}),
        ToolCall("show_map", {"query": "a@example.com"}),
    ]

    rows = per_tool_summary(golds, preds, model="babyB", eval_set="smoke")

    by_tool = {row["tool"]: row for row in rows}
    assert by_tool["show_map"]["n"] == 2
    assert by_tool["show_map"]["function_accuracy"] == 1.0
    assert by_tool["show_map"]["tool_call_exact_match"] == 0.5
    assert by_tool["send_email"]["n"] == 1
    assert by_tool["send_email"]["function_accuracy"] == 0.0

