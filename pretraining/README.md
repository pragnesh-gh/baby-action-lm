# BabyA and BabyB pretraining provenance

BabyActionLM fine-tunes two small causal language models that were pretrained from scratch as preliminary models for this project. Their training code was adapted from the course's LLaMA-from-scratch materials. The relevant source is included here so the relationship between base-model pretraining and downstream Mobile Actions fine-tuning is visible in one place.

## Included source

- `ModelA-llama-from-scratch.ipynb` trains BabyA on the smaller pretraining corpus.
- `ModelB-llama-from-scratch.ipynb` trains BabyB on the larger pretraining corpus.
- `normalize_and_merge.py` cleans individual Project Gutenberg texts and combines them into model corpora.

The notebooks are output-stripped copies of the executed model-development notebooks from commit `99f22c1` of `pragnesh-gh/Neural_Networks_For_NLP_Course`. Saved cell outputs were removed here to keep the project reviewable; the source cells were retained. The historical local paths in the notebooks must be changed when running them elsewhere.

## Pretraining data

Both corpora were assembled from public-domain Project Gutenberg texts and cleaned with `normalize_and_merge.py`.

- Corpus A: approximately 2 MB; Gutenberg IDs `pg11`, `pg43`, and `pg145`.
- Corpus B: approximately 20 MB; Gutenberg IDs `pg84`, `pg394`, `pg100`, `pg1259`, `pg1260`, `pg1342`, `pg1513`, `pg1661`, `pg2160`, `pg2641`, `pg4085`, `pg5197`, `pg6593`, `pg6761`, `pg7241`, `pg16328`, `pg16389`, `pg16865`, `pg37106`, and `pg2701`.
- A shared tokenizer was trained on the union of Corpus A and Corpus B.

The raw and merged text files are not duplicated in Git. They can be reconstructed from the public source texts with the included normalization script.

## Shared model setup

The notebooks use the same architecture and training settings for both models so that the primary difference is pretraining data volume:

- LLaMA-style causal language model
- vocabulary size: 8,000
- hidden size: 128
- four transformer layers
- four attention heads
- context length: 128 tokens
- 25 training epochs
- learning rate: `3e-4`
- batch size: 16 with eight gradient-accumulation steps

The notebooks save Hugging Face-compatible model and tokenizer directories. BabyActionLM then loads those base directories through `base_model_dir` in its experiment configurations and performs task-specific fine-tuning on `google/mobile-actions`.

Model weights, optimizer states, downstream checkpoints, and raw predictions are generated artifacts and are intentionally excluded from this repository. The tracked configs and source code document how they were produced.
