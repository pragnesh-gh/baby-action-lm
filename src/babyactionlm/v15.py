from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable


def choose_best_trial(trials: Iterable[dict[str, object]]) -> dict[str, object]:
    trial_list = list(trials)
    if not trial_list:
        raise ValueError("no trials to choose from")
    return max(
        trial_list,
        key=lambda row: (
            float(row.get("tool_call_exact_match", 0.0) or 0.0),
            float(row.get("function_accuracy", 0.0) or 0.0),
            float(row.get("parse_rate", 0.0) or 0.0),
        ),
    )


def _read_first_row(path: str | Path) -> dict[str, str]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"empty summary file: {path}")
    return rows[0]


def build_trial_table(summary_paths: Iterable[str | Path]) -> tuple[list[dict[str, str]], dict[str, str]]:
    rows: list[dict[str, str]] = []
    for summary_path in summary_paths:
        row = _read_first_row(summary_path)
        row["trial"] = row.get("model", Path(summary_path).stem.replace("-summary", ""))
        row["source_file"] = str(summary_path)
        row["selected"] = "false"
        rows.append(row)
    best = choose_best_trial(rows)
    best_trial = str(best["trial"])
    for row in rows:
        row["selected"] = "true" if row["trial"] == best_trial else "false"
    return rows, next(row for row in rows if row["selected"] == "true")


def write_trial_table(path: str | Path, rows: list[dict[str, str]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("no trial rows to write")
    columns = list(rows[0].keys())
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and select BabyActionLM v1.5 dev trials.")
    parser.add_argument("summaries", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=Path("results/v15_trials.csv"))
    args = parser.parse_args()
    rows, best = build_trial_table(args.summaries)
    write_trial_table(args.output, rows)
    print(
        "Selected {trial}: exact={exact}, function={function}, parse={parse}".format(
            trial=best["trial"],
            exact=best.get("tool_call_exact_match", ""),
            function=best.get("function_accuracy", ""),
            parse=best.get("parse_rate", ""),
        )
    )


if __name__ == "__main__":
    main()
