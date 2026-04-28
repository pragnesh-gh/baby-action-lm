from babyactionlm.train import build_causal_lm_features


class TinyTokenizer:
    eos_token = "<eos>"
    pad_token_id = 0

    def __call__(self, text, add_special_tokens=False):
        del add_special_tokens
        vocab = {"A": 10, "B": 11, "C": 12, "X": 20, "Y": 21, "<eos>": 99}
        return {"input_ids": [vocab[token] for token in text.split()]}


def test_build_causal_lm_features_masks_prompt_tokens_and_pads():
    features = build_causal_lm_features("A B C", "X Y", TinyTokenizer(), max_length=8)

    assert features["input_ids"] == [10, 11, 12, 20, 21, 99, 0, 0]
    assert features["labels"] == [-100, -100, -100, 20, 21, 99, -100, -100]
    assert features["attention_mask"] == [1, 1, 1, 1, 1, 1, 0, 0]


def test_build_causal_lm_features_trims_prompt_but_preserves_target():
    features = build_causal_lm_features("A B C", "X Y", TinyTokenizer(), max_length=5)

    assert features["input_ids"] == [11, 12, 20, 21, 99]
    assert features["labels"] == [-100, -100, 20, 21, 99]
