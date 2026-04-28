from babyactionlm.data import MobileActionRecord, select_eval_records, split_records, to_records


def _row(split, command, tool_name="show_map"):
    return {
        "metadata": split,
        "tools": [{"function": {"name": tool_name, "parameters": {"properties": {"query": {}}}}}],
        "messages": [
            {"role": "developer", "content": "date context"},
            {"role": "user", "content": command},
            {
                "role": "assistant",
                "tool_calls": [{"function": {"name": tool_name, "arguments": {"query": command}}}],
            },
        ],
    }


def test_to_records_assigns_stable_ids_and_keeps_lightweight_fields():
    records = to_records([_row("train", "Find the library"), _row("eval", "Find the station")])

    assert records[0] == MobileActionRecord(
        id="mobile-actions-000000",
        split="train",
        tools=[{"function": {"name": "show_map", "parameters": {"properties": {"query": {}}}}}],
        messages=[
            {"role": "developer", "content": "date context"},
            {"role": "user", "content": "Find the library"},
            {
                "role": "assistant",
                "tool_calls": [{"function": {"name": "show_map", "arguments": {"query": "Find the library"}}}],
            },
        ],
    )
    assert records[1].id == "mobile-actions-000001"


def test_split_records_uses_metadata_split_values():
    records = to_records([_row("train", "A"), _row("eval", "B"), _row("train", "C")])

    train, eval_records = split_records(records)

    assert [record.split for record in train] == ["train", "train"]
    assert [record.split for record in eval_records] == ["eval"]


def test_select_eval_records_uses_all_rows_when_under_cap():
    records = to_records([_row("eval", "A"), _row("eval", "B")])

    selected = select_eval_records(records, cap=1000, seed=42)

    assert [record.id for record in selected] == ["mobile-actions-000000", "mobile-actions-000001"]


def test_select_eval_records_stratifies_by_gold_tool_when_capped():
    records = to_records(
        [
            _row("eval", "A1", "show_map"),
            _row("eval", "A2", "show_map"),
            _row("eval", "B1", "send_email"),
            _row("eval", "B2", "send_email"),
        ]
    )

    selected = select_eval_records(records, cap=2, seed=42)

    assert len(selected) == 2
    assert {record.messages[2]["tool_calls"][0]["function"]["name"] for record in selected} == {
        "show_map",
        "send_email",
    }

