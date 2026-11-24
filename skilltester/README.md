# Skilltester

Score a model’s text replies against expected behavior for an agent skill. Reports group results by tags such as difficulty.

From `skilltester/`, set the model and endpoint in the [example config](examples/imperative/config.py) and run with `uv`.

```bash
uv run skilltester --skill ../skills/imperative/SKILL.md
```

Use `--config` and `--examples` to override suite discovery. Tool calls and file changes require separate checks. [Specification](SPEC.md)
