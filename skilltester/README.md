# Skilltester

Minimal async testing for arbitrary agent skills, powered by NOOA.

Everything is Python: model configuration, examples, execution, and results. See [`SPEC.md`](SPEC.md).

```bash
uv sync
uv run skilltester \
  --skill ../skills/imperative/SKILL.md \
  --config examples/imperative/config.py \
  --examples examples/imperative/examples.py
```

With exactly one local `SKILL.md` and one matching `config.py`/`examples.py` pair, flags are optional:

```bash
skilltester
```

`examples.py` is dependency-free Python data. It exports the candidate system prompt, four response-type definitions, and examples containing `prompt`, `expected_response_type`, and optional `tags`. Prompts may be strings or multi-turn message lists. Skilltester owns the fixed judge instruction.

An optional `Tags(TypedDict)` with required `Literal` fields defines categorical tags. Skilltester validates every tag dictionary and reports scores grouped by each allowed value.

All candidate requests start concurrently; each judge starts as soon as its corresponding response arrives. An optional `truth_table` can assign partial credit between response types; absent that, matching is exact.

`config.py` exports one `llm` value: either a single NOOA client for both roles or a dictionary containing exactly `candidate` and `judge` clients.

`--skill` selects a `SKILL.md` file. Without it, Skilltester searches the current directory recursively. It then discovers the `config.py`/`examples.py` pair whose directory matches the skill name. Explicit flags override discovery. Skilltester reads the selected skill and appends its raw text to `system_prompt` once at the beginning of every candidate conversation.
