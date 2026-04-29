from pathlib import Path

from babyactionlm.v15 import build_trial_table, choose_best_trial


def test_choose_best_trial_prefers_exact_then_function_then_parse_rate():
    trials = [
        {"name": "json_8", "tool_call_exact_match": 0.1, "function_accuracy": 0.9, "parse_rate": 1.0},
        {"name": "dsl_3", "tool_call_exact_match": 0.2, "function_accuracy": 0.4, "parse_rate": 0.5},
        {"name": "dsl_8", "tool_call_exact_match": 0.2, "function_accuracy": 0.5, "parse_rate": 0.4},
    ]

    assert choose_best_trial(trials)["name"] == "dsl_8"


def test_build_trial_table_combines_summary_files():
    fixture_dir = Path("outputs/unit-test-v15")
    fixture_dir.mkdir(parents=True, exist_ok=True)
    first = fixture_dir / "json-summary.csv"
    second = fixture_dir / "dsl-summary.csv"
    first.write_text(
        "model,parse_rate,function_accuracy,argument_exact_match,tool_call_exact_match\n"
        "babyB-v15-json-3,0.8,0.2,0.1,0.1\n",
        encoding="utf-8",
    )
    second.write_text(
        "model,parse_rate,function_accuracy,argument_exact_match,tool_call_exact_match\n"
        "babyB-v15-dsl-3,0.9,0.3,0.2,0.2\n",
        encoding="utf-8",
    )

    rows, best = build_trial_table([first, second])

    assert [row["trial"] for row in rows] == ["babyB-v15-json-3", "babyB-v15-dsl-3"]
    assert best["trial"] == "babyB-v15-dsl-3"
    assert best["selected"] == "true"
