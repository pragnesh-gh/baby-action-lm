from babyactionlm.evaluate import prepare_generation_inputs, tokenize_prompt_for_generation


def test_prepare_generation_inputs_drops_token_type_ids_for_llama_generation():
    inputs = {
        "input_ids": [1, 2, 3],
        "attention_mask": [1, 1, 1],
        "token_type_ids": [0, 0, 0],
    }

    prepared = prepare_generation_inputs(inputs)

    assert prepared == {"input_ids": [1, 2, 3], "attention_mask": [1, 1, 1]}


class CountingTokenizer:
    pad_token_id = 0

    def __call__(self, prompt, return_tensors=None, truncation=False, max_length=None):
        del prompt, return_tensors
        ids = list(range(10))
        if truncation:
            ids = ids[-max_length:]
        return {"input_ids": [ids], "attention_mask": [[1] * len(ids)], "token_type_ids": [[0] * len(ids)]}


def test_tokenize_prompt_for_generation_leaves_room_for_new_tokens():
    inputs = tokenize_prompt_for_generation(
        CountingTokenizer(),
        "ignored",
        model_max_length=8,
        max_new_tokens=3,
    )

    assert inputs["input_ids"] == [[5, 6, 7, 8, 9]]
    assert "token_type_ids" not in inputs
