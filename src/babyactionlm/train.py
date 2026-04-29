from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from babyactionlm.config import load_yaml
from babyactionlm.data import load_mobile_actions, split_records, split_train_dev_records
from babyactionlm.formatting import FormattedExample, format_example


def build_causal_lm_features(prompt: str, target: str, tokenizer: Any, max_length: int) -> dict[str, list[int]]:
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    eos = f" {tokenizer.eos_token}" if getattr(tokenizer, "eos_token", None) else ""
    target_ids = tokenizer(f"{target}{eos}", add_special_tokens=False)["input_ids"]
    if len(target_ids) >= max_length:
        raise ValueError("target is too long for max_length")

    prompt_budget = max_length - len(target_ids)
    prompt_ids = prompt_ids[-prompt_budget:]
    input_ids = prompt_ids + target_ids
    labels = [-100] * len(prompt_ids) + target_ids
    attention_mask = [1] * len(input_ids)

    pad_token_id = tokenizer.pad_token_id
    padding = max_length - len(input_ids)
    if padding > 0:
        input_ids.extend([pad_token_id] * padding)
        labels.extend([-100] * padding)
        attention_mask.extend([0] * padding)

    return {"input_ids": input_ids, "labels": labels, "attention_mask": attention_mask}


def _limit(items: list[Any], limit: int | None) -> list[Any]:
    return items[:limit] if limit else items


def encode_examples(
    examples: list[FormattedExample],
    tokenizer: Any,
    max_length: int,
) -> list[dict[str, list[int]]]:
    encoded = []
    for example in examples:
        try:
            encoded.append(build_causal_lm_features(example.prompt, example.target, tokenizer, max_length))
        except ValueError:
            continue
    return encoded


def precision_flags() -> dict[str, bool]:
    import torch

    if not torch.cuda.is_available():
        return {"bf16": False, "fp16": False}
    return {"bf16": bool(torch.cuda.is_bf16_supported()), "fp16": not bool(torch.cuda.is_bf16_supported())}


def _training_args(output_dir: str, config: dict[str, Any]):
    from transformers import TrainingArguments

    kwargs = {
        "output_dir": output_dir,
        "num_train_epochs": config.get("num_train_epochs", 3),
        "per_device_train_batch_size": config.get("per_device_train_batch_size", 4),
        "per_device_eval_batch_size": config.get("per_device_eval_batch_size", 4),
        "gradient_accumulation_steps": config.get("gradient_accumulation_steps", 8),
        "learning_rate": config.get("learning_rate", 5e-5),
        "logging_steps": config.get("logging_steps", 10),
        "save_strategy": config.get("save_strategy", "epoch"),
        "eval_strategy": config.get("eval_strategy", "epoch"),
        "save_total_limit": config.get("save_total_limit", 2),
        "report_to": [],
        **precision_flags(),
    }
    try:
        return TrainingArguments(**kwargs)
    except TypeError:
        kwargs["evaluation_strategy"] = kwargs.pop("eval_strategy")
        return TrainingArguments(**kwargs)


def train_from_config(config_path: str | Path) -> None:
    from datasets import Dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer

    config = load_yaml(config_path)
    max_length = int(config.get("max_length", 128))
    target_format = str(config.get("target_format", "json_v1"))
    tokenizer = AutoTokenizer.from_pretrained(config["base_model_dir"])
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(config["base_model_dir"])

    records = load_mobile_actions()
    if config.get("validation_source") == "dev":
        train_records, eval_records = split_train_dev_records(
            records,
            dev_size=float(config.get("dev_size", 0.1)),
            seed=int(config.get("seed", 42)),
        )
    else:
        train_records, eval_records = split_records(records)
    train_examples = [
        format_example(record, target_format=target_format)
        for record in _limit(train_records, config.get("train_limit"))
    ]
    eval_examples = [
        format_example(record, target_format=target_format)
        for record in _limit(eval_records, config.get("eval_limit"))
    ]
    train_dataset = Dataset.from_list(encode_examples(train_examples, tokenizer, max_length))
    eval_dataset = Dataset.from_list(encode_examples(eval_examples, tokenizer, max_length))

    trainer = Trainer(
        model=model,
        args=_training_args(config["output_dir"], config),
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    trainer.train()
    trainer.save_model(config["output_dir"])
    tokenizer.save_pretrained(config["output_dir"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune BabyA/B on Mobile Actions.")
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    train_from_config(args.config)


if __name__ == "__main__":
    main()
