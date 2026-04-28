import json
from pathlib import Path

from babyactionlm.analysis import collect_qualitative_examples, combine_csv_files


def _test_dir(name):
    path = Path("outputs/test-analysis") / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_combine_csv_files_preserves_rows_and_adds_source():
    base = _test_dir("combine")
    first = base / "a.csv"
    second = base / "b.csv"
    first.write_text("model,n\nbabyA,1\n", encoding="utf-8")
    second.write_text("model,n\nbabyB,2\n", encoding="utf-8")

    combined = combine_csv_files([first, second])

    assert combined[0]["model"] == "babyA"
    assert combined[0]["source_file"] == "a.csv"
    assert combined[1]["model"] == "babyB"


def test_collect_qualitative_examples_returns_wrong_and_correct_rows():
    raw = _test_dir("qualitative") / "predictions.jsonl"
    rows = [
        {
            "id": "1",
            "command": "Turn on flashlight",
            "gold": {"name": "turn_on_flashlight", "arguments": {}},
            "prediction": {"name": "turn_on_flashlight", "arguments": {}, "parse_error": None},
            "raw_text": "{}",
        },
        {
            "id": "2",
            "command": "Open Wi-Fi",
            "gold": {"name": "open_wifi_settings", "arguments": {}},
            "prediction": {"name": "show_map", "arguments": {"query": "Wi-Fi"}, "parse_error": None},
            "raw_text": "{}",
        },
    ]
    raw.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    examples = collect_qualitative_examples([raw], limit_per_bucket=2)

    assert examples["correct"][0]["id"] == "1"
    assert examples["wrong_tool"][0]["id"] == "2"
