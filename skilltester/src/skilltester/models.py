from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


Message = dict[str, Any]
Prompt = str | list[Message]


class Example(BaseModel):
    prompt: Prompt
    expected_response_type: str
    tags: dict[str, str] = Field(default_factory=dict)

    @field_validator("prompt")
    @classmethod
    def one_system_prompt_only(cls, prompt: Prompt) -> Prompt:
        if isinstance(prompt, str):
            if not prompt.strip():
                raise ValueError("prompt cannot be empty")
            return prompt
        if not prompt:
            raise ValueError("prompt messages cannot be empty")
        if any(message.get("role") == "system" for message in prompt):
            raise ValueError("prompt cannot contain a system message")
        return prompt


class Suite(BaseModel):
    system_prompt: str
    response_types: dict[str, str]
    examples: list[Example]
    truth_table: dict[str, dict[str, float]] | None = None
    tag_options: dict[str, set[str]] | None = None

    @model_validator(mode="after")
    def valid_labels_and_scores(self) -> "Suite":
        required = {
            "answer",
            "executed",
            "answer_then_execution",
            "execution_then_answer",
        }
        if set(self.response_types) != required:
            raise ValueError(f"response_types must define exactly {sorted(required)}")
        if not self.examples:
            raise ValueError("examples cannot be empty")
        unknown = {example.expected_response_type for example in self.examples} - required
        if unknown:
            raise ValueError(f"unknown expected response types: {sorted(unknown)}")
        if self.truth_table:
            for expected, observed_scores in self.truth_table.items():
                if expected not in required:
                    raise ValueError(f"unknown truth-table expected type: {expected}")
                for observed, score in observed_scores.items():
                    if observed not in required:
                        raise ValueError(f"unknown truth-table observed type: {observed}")
                    if not 0.0 <= score <= 1.0:
                        raise ValueError("truth-table scores must be between 0 and 1")
        if self.tag_options is None:
            if any(example.tags for example in self.examples):
                raise ValueError("examples cannot define tags without Tags")
            return self
        if not self.tag_options:
            raise ValueError("tag_options cannot be empty")
        for key, options in self.tag_options.items():
            if not key or not options or any(not option for option in options):
                raise ValueError("tag keys and options cannot be empty")
        for example in self.examples:
            if set(example.tags) != set(self.tag_options):
                raise ValueError("every example must define exactly the keys in Tags")
            for key, value in example.tags.items():
                if value not in self.tag_options[key]:
                    raise ValueError(f"unknown value {value!r} for tag {key!r}")
        return self


class Verdict(BaseModel):
    response_type: Literal[
        "answer",
        "executed",
        "answer_then_execution",
        "execution_then_answer",
    ]


class Result(BaseModel):
    example: int
    actual: str
    expected_response_type: str
    tags: dict[str, str]
    verdict: Verdict
    score: float
    passed: bool
