from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class MobileActionRecord:
    id: str
    split: str
    tools: list[dict]
    messages: list[dict]


def to_records(rows: Iterable[dict]) -> list[MobileActionRecord]:
    records: list[MobileActionRecord] = []
    for index, row in enumerate(rows):
        records.append(
            MobileActionRecord(
                id=f"mobile-actions-{index:06d}",
                split=str(row["metadata"]),
                tools=list(row["tools"]),
                messages=list(row["messages"]),
            )
        )
    return records


def load_mobile_actions(split: str = "train") -> list[MobileActionRecord]:
    from datasets import load_dataset

    return to_records(load_dataset("google/mobile-actions", split=split))


def split_records(records: Sequence[MobileActionRecord]) -> tuple[list[MobileActionRecord], list[MobileActionRecord]]:
    train = [record for record in records if record.split == "train"]
    eval_records = [record for record in records if record.split == "eval"]
    return train, eval_records


def gold_tool_name(record: MobileActionRecord) -> str:
    return record.messages[2]["tool_calls"][0]["function"]["name"]


def select_eval_records(records: Sequence[MobileActionRecord], cap: int = 1000, seed: int = 42) -> list[MobileActionRecord]:
    eval_records = [record for record in records if record.split == "eval"]
    if len(eval_records) <= cap:
        return list(eval_records)

    by_tool: dict[str, list[MobileActionRecord]] = defaultdict(list)
    for record in eval_records:
        by_tool[gold_tool_name(record)].append(record)

    rng = random.Random(seed)
    selected: list[MobileActionRecord] = []
    tools = sorted(by_tool)
    base_quota = cap // len(tools)
    remainder = cap % len(tools)
    for index, tool in enumerate(tools):
        quota = base_quota + (1 if index < remainder else 0)
        bucket = list(by_tool[tool])
        rng.shuffle(bucket)
        selected.extend(bucket[:quota])

    selected.sort(key=lambda record: record.id)
    return selected[:cap]

