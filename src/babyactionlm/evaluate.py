from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from babyactionlm.config import load_yaml
from babyactionlm.data import load_mobile_actions, select_eval_records
from babyactionlm.formatting import format_example
from babyactionlm.metrics import per_tool_summary, score_predictions
from babyactionlm.reporting import write_per_tool_csv, write_summary_csv
from babyactionlm.schema import from_dataset_function, parse_tool_call


def prepare_generation_inputs(inputs: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in inputs.items() if key != "token_type_ids"}


def tokenize_prompt_for_generation(
    tokenizer: Any,
    prompt: str,
    *,
    model_max_length: int,
    max_new_tokens: int,
) -> dict[str, Any]:
    prompt_length = max(1, model_max_length - max_new_tokens)
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=prompt_length,
    )
    return prepare_generation_inputs(inputs)


def generate_text(model: Any, tokenizer: Any, prompt: str, max_new_tokens: int) -> str:
    import torch

    model_max_length = int(getattr(model.config, "max_position_embeddings", 128))
    inputs = tokenize_prompt_for_generation(
        tokenizer,
        prompt,
        model_max_length=model_max_length,
        max_new_tokens=max_new_tokens,
    )
    inputs = {key: value.to(model.device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    generated = outputs[0][inputs["input_ids"].shape[-1] :]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def evaluate_from_config(config_path: str | Path) -> None:
    from transformers import AutoModelForCausalLM, AutoTokenizer

    config = load_yaml(config_path)
    model_dir = config["model_dir"]
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(model_dir)
    model.eval()

    records = select_eval_records(load_mobile_actions(), cap=int(config.get("eval_cap", 1000)), seed=int(config.get("seed", 42)))
    if config.get("eval_limit"):
        records = records[: int(config["eval_limit"])]

    golds = []
    preds = []
    raw_rows = []
    for record in records:
        example = format_example(record)
        gold = from_dataset_function(record.messages[2]["tool_calls"][0]["function"])
        text = generate_text(model, tokenizer, example.prompt, int(config.get("max_new_tokens", 64)))
        pred = parse_tool_call(text)
        golds.append(gold)
        preds.append(pred)
        raw_rows.append(
            {
                "id": record.id,
                "command": record.messages[1]["content"],
                "gold": gold.__dict__,
                "prediction": pred.__dict__,
                "raw_text": text,
            }
        )

    timestamp = datetime.now().isoformat(timespec="seconds")
    summary = score_predictions(
        golds,
        preds,
        model=str(config.get("model_name", Path(model_dir).name)),
        checkpoint=model_dir,
        eval_set=str(config.get("eval_set", "eval")),
        timestamp=timestamp,
        config_path=str(config_path),
    )
    raw_path = Path(config.get("raw_predictions_path", "outputs/predictions/eval_predictions.jsonl"))
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    with raw_path.open("w", encoding="utf-8") as handle:
        for row in raw_rows:
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")

    write_summary_csv(config.get("summary_path", "results/summary.csv"), [summary])
    write_per_tool_csv(
        config.get("per_tool_path", "results/per_tool.csv"),
        per_tool_summary(golds, preds, model=str(summary["model"]), eval_set=str(summary["eval_set"])),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate BabyActionLM checkpoints.")
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    evaluate_from_config(args.config)


if __name__ == "__main__":
    main()
