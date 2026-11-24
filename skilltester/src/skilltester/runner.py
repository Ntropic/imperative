import asyncio
import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .models import Example, Result, Suite, Verdict


JUDGE_SYSTEM_PROMPT = """Classify what the candidate actually did using the prompt and the supplied response types.
Use the prompt to interpret the response. Do not infer completion from the request or from a promise.
Return only the structured classification."""


def _prompt_messages(prompt: str | list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt


def _text(content: str | BaseModel) -> str:
    return content if isinstance(content, str) else content.model_dump_json()


def _clients(llm: Any) -> tuple[Any, Any]:
    if isinstance(llm, dict):
        if set(llm) != {"candidate", "judge"}:
            raise ValueError("llm dictionary must contain exactly 'candidate' and 'judge'")
        candidate, judge = llm["candidate"], llm["judge"]
    else:
        candidate = judge = llm
    if not all(callable(getattr(client, "acall", None)) for client in (candidate, judge)):
        raise TypeError("each llm client must provide acall()")
    return candidate, judge


async def _run_one(
    number: int,
    example: Example,
    skill: str,
    suite: Suite,
    candidate_llm: Any,
    judge_llm: Any,
) -> Result:
    candidate_messages = [
        {"role": "system", "content": f"{suite.system_prompt}\n\n{skill}"},
        *_prompt_messages(example.prompt),
    ]
    response = await candidate_llm.acall(candidate_messages)
    actual = _text(response.content)

    review_input = {
        "prompt": example.prompt,
        "actual": actual,
        "response_types": suite.response_types,
    }
    review = await judge_llm.acall(
        [
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(review_input, ensure_ascii=False)},
        ],
        output_model=Verdict,
    )
    verdict = getattr(review, "parsed", None)
    if not isinstance(verdict, Verdict):
        verdict = review.content
    if not isinstance(verdict, Verdict):
        raise TypeError("judge did not return a Verdict")
    observed = verdict.response_type
    score = (
        suite.truth_table.get(example.expected_response_type, {}).get(
            observed,
            float(example.expected_response_type == observed),
        )
        if suite.truth_table
        else float(example.expected_response_type == observed)
    )
    return Result(
        example=number,
        actual=actual,
        expected_response_type=example.expected_response_type,
        tags=example.tags,
        verdict=verdict,
        score=score,
        passed=score == 1.0,
    )


async def run(
    *,
    skill: str | Path,
    suite: Suite,
    llm: Any,
) -> list[Result]:
    skill_text = Path(skill).read_text(encoding="utf-8")
    candidate, judge = _clients(llm)
    return await asyncio.gather(
        *(
            _run_one(
                number,
                example,
                skill_text,
                suite,
                candidate,
                judge,
            )
            for number, example in enumerate(suite.examples, start=1)
        )
    )


def build_report(
    results: list[Result],
    tag_options: dict[str, set[str]] | None = None,
) -> dict[str, Any]:
    report: dict[str, Any] = {
        "results": [result.model_dump() for result in results],
    }
    if tag_options is None:
        return report

    report["tag_options"] = {
        key: sorted(options) for key, options in tag_options.items()
    }

    def summary(group: list[Result]) -> dict[str, int | float | None]:
        return {
            "count": len(group),
            "passed": sum(result.passed for result in group),
            "average_score": (
                sum(result.score for result in group) / len(group) if group else None
            ),
        }

    report["summary_by_tag"] = {
        key: {
            value: summary(
                [result for result in results if result.tags.get(key) == value]
            )
            for value in sorted(options)
        }
        for key, options in tag_options.items()
    }
    return report
