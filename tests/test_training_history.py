import json
from pathlib import Path

from babyactionlm.training_history import extract_trainer_history


def test_extract_trainer_history_reads_train_and_eval_loss_rows():
    state_path = Path("outputs/test-training-history/trainer_state.json")
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "log_history": [
                    {"step": 10, "epoch": 0.1, "loss": 2.5, "learning_rate": 1e-5},
                    {"step": 20, "epoch": 1.0, "eval_loss": 2.0},
                ]
            }
        ),
        encoding="utf-8",
    )

    rows = extract_trainer_history("babyB", state_path)

    assert rows == [
        {"model": "babyB", "step": 10, "epoch": 0.1, "metric": "train_loss", "value": 2.5},
        {"model": "babyB", "step": 20, "epoch": 1.0, "metric": "eval_loss", "value": 2.0},
    ]

