from pathlib import Path

from babyactionlm.reporting import write_per_tool_csv, write_summary_csv


def test_write_summary_csv_creates_expected_header():
    output_dir = Path("outputs/test-reporting")
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "summary.csv"

    write_summary_csv(
        output,
        [
            {
                "model": "babyB",
                "checkpoint": "outputs/checkpoint",
                "eval_set": "smoke",
                "n": 32,
                "parse_rate": 0.5,
                "function_accuracy": 0.4,
                "argument_exact_match": 0.3,
                "tool_call_exact_match": 0.2,
                "timestamp": "2026-04-28T00:00:00",
                "config_path": "experiments/configs/smoke.yaml",
            }
        ],
    )

    assert output.read_text().splitlines()[0] == (
        "model,checkpoint,eval_set,n,parse_rate,function_accuracy,"
        "argument_exact_match,tool_call_exact_match,timestamp,config_path"
    )


def test_write_per_tool_csv_creates_parent_directory():
    output = Path("outputs/test-reporting/nested/per_tool.csv")

    write_per_tool_csv(
        output,
        [
            {
                "model": "babyB",
                "eval_set": "smoke",
                "tool": "show_map",
                "n": 1,
                "parse_rate": 1.0,
                "function_accuracy": 1.0,
                "argument_exact_match": 1.0,
                "tool_call_exact_match": 1.0,
            }
        ],
    )

    assert Path(output).exists()
