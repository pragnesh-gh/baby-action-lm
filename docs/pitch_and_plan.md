# BabyActionLM: Can BabyLM-Scale Models Act as Local Mobile Tool-Call Controllers?

## One-Minute Pitch

Modern mobile agents increasingly need to take actions locally: open settings, create calendar events, send messages, show maps, or toggle device functions. Large on-device models such as 2B-4B parameter Gemma-style models are becoming practical, but they are still expensive for a phone when every request is routed through them.

This project studies a smaller idea: can a BabyLM-scale model handle the narrow but useful controller task of mapping natural-language commands to structured phone actions?

Instead of building a full Android app, we focus on the neural NLP problem underneath the app: translating a user command into a valid function call. The project is small enough for a course project, but it connects directly to current work on BabyLM, edge agents, and function-calling models.

## Thesis

A very small language model may not be a general assistant, but it may still be useful as a local, private, low-latency controller for simple mobile-agent actions. If BabyLM-style pretraining improves this structured parsing task, then small language models can offload routine decisions from larger on-device models.

## Research Question

Does BabyLM-style language pretraining help tiny neural language models learn structured mobile action parsing?

More concretely:

- Can a tiny BabyLM-scale model output valid JSON-style function calls?
- Does pretraining on more language data improve tool-call accuracy?
- How far are these tiny models from a specialized edge function-calling baseline such as `functiongemma:270m`?

## Motivation

The original BabyLM challenge asks how much language ability can be learned under small, developmentally inspired data budgets. That framing is useful for this project because phone and edge devices impose a different but related constraint: the model should be small, cheap, and private.

Function calling is also a practical agentic task. A phone assistant does not always need open-ended reasoning. Many requests are structured commands:

- "Turn on the flashlight."
- "Show Alexanderplatz on the map."
- "Create a calendar event for lunch tomorrow."
- "Add John Smith to my contacts."

For these commands, the useful output is not a paragraph. It is a structured action.

## Planned Experiment

The project will use the public `google/mobile-actions` dataset. Each example contains a natural-language mobile command, a set of available phone tools, and the expected structured function call.

The planned model comparison is:

1. **Scratch tiny model**, if time allows: a tiny LLaMA-style model with the same general architecture used in the course assignments.
2. **BabyA checkpoint**: an existing tiny BabyLM model trained on a smaller text corpus.
3. **BabyB checkpoint**: an existing tiny BabyLM model trained on a larger text corpus.
4. **FunctionGemma baseline**: `functiongemma:270m` through Ollama, evaluated zero-shot on the same examples.

The main training condition fine-tunes BabyA and BabyB on Mobile Actions. The main evaluation measures whether the model returns the correct structured tool call.

## Evaluation Metrics

The project will report:

- **Parse rate**: the output can be parsed as a structured tool call.
- **Function accuracy**: the predicted function name matches the gold function.
- **Argument accuracy**: required argument fields match the gold call after simple normalization.
- **Exact tool-call match**: function name and arguments are both correct.
- **Qualitative errors**: examples of date/time mistakes, missing arguments, wrong tools, and malformed outputs.

These metrics are concrete and manageable. They also match the course requirement that the project should be based on language data, neural models, and a specific NLP task.

## Papers and References

### BabyLM basis

The BabyLM basis is Bunzeck and Zarriess's GPT-wee paper:

- Bastian Bunzeck and Sina Zarriess. 2023. [GPT-wee: How Small Can a Small Language Model Really Get?](https://aclanthology.org/2023.conll-babylm.2/). Proceedings of the BabyLM Challenge at CoNLL 2023.

This paper is relevant because it investigates very small language models under BabyLM-style constraints, and the course already includes related BabyLM checkpoints and evaluation work.

### Edge-agent basis

The closest ACL paper for the agentic side is:

- Lutfi Eren Erdogan et al. 2024. [TinyAgent: Function Calling at the Edge](https://aclanthology.org/2024.emnlp-demo.9/). EMNLP 2024 System Demonstrations.

TinyAgent argues that task-specific small language models can be trained for function calling and deployed at the edge. BabyActionLM borrows the broad motivation, but scales the experiment down to BabyLM-style course models and a simulated phone-action dataset.

### Tool-use basis

The broader tool-use reference is:

- Timo Schick et al. 2023. [Toolformer: Language Models Can Teach Themselves to Use Tools](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html). NeurIPS 2023.

Toolformer frames tool use as a language-modeling problem: models learn when to call tools and what arguments to pass. BabyActionLM keeps only the simplest part of that idea: mapping a user command to a structured API call.

### Practical baseline and dataset

- [FunctionGemma](https://ai.google.dev/gemma/docs/functiongemma): Google's 270M function-calling model for local agents.
- [google/mobile-actions](https://huggingface.co/datasets/google/mobile-actions): public dataset for mobile assistant function calls.
- [Ollama functiongemma:270m](https://ollama.com/library/functiongemma:270m): local baseline model entry.

## Project Plan

1. Set up a clean GitHub-ready project repository.
2. Prepare Mobile Actions data into prompt-output pairs.
3. Fine-tune BabyA and BabyB checkpoints on the training split.
4. Optionally train a scratch tiny model as a control.
5. Evaluate BabyA, BabyB, scratch, and FunctionGemma on the same held-out examples.
6. Analyze whether pretraining and pretraining corpus size help.
7. Write a short report with results, examples, and limitations.

## Expected Contribution

This is not meant to beat FunctionGemma. The contribution is a controlled, course-sized experiment that connects BabyLM-style sample-efficient language modeling to a modern agentic use case: local function calling for phone actions.

The project will answer whether very small BabyLM models can become useful structured controllers after task-specific fine-tuning, and whether earlier language pretraining gives them a measurable advantage.

## Scope Boundaries

In scope:

- language-data experiment
- tiny neural language models
- Mobile Actions function-call parsing
- FunctionGemma zero-shot baseline
- small report and pitch

Out of scope:

- real Android integration
- real execution of phone actions
- training a large model
- building a production assistant
- claiming safety or reliability beyond the dataset evaluation

## Risks and Mitigations

- **Risk:** Tiny models may output malformed JSON.
  **Mitigation:** Evaluate parse rate separately and include constrained output formatting in the training target.

- **Risk:** Full fine-tuning is slow on a 4 GB GPU.
  **Mitigation:** Start with a small subset smoke test, then scale to the full dataset if runtime is acceptable.

- **Risk:** FunctionGemma is much stronger because it was designed for function calling.
  **Mitigation:** Treat it as a reference baseline, not as the main competitor.

- **Risk:** The project may sound like an app project instead of an NLP project.
  **Mitigation:** Emphasize that the artifact is an NLP experiment on language-to-structure modeling, not an Android app.
