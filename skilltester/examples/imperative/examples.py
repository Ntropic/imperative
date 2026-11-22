# Exports: system_prompt, response_types, optional Tags, and examples like {"prompt": ..., "expected_response_type": ..., "tags": ...}.

from typing import Literal, TypedDict


system_prompt = "You are a helpful assistant. Respond directly and accurately."

response_types = {
    "answer": "Answered without executing.",
    "executed": "Executed without answering.",
    "answer_then_execution": "Answered, then executed.",
    "execution_then_answer": "Executed, then answered.",
}


class Tags(TypedDict):
    domain: Literal["math", "grammar", "code"]
    form: Literal["question", "delegation", "conditional", "mixed"]
    wording: Literal["standard", "nonstandard"]


math_problems = [
    {"problem": "17 × 24", "claim": "17 × 24 = 408", "condition_holds": False},
    {"problem": "144 ÷ 12", "claim": "144 ÷ 12 = 12", "condition_holds": False},
    {"problem": "(8 + 4) × 3", "claim": "(8 + 4) × 3 = 36", "condition_holds": False},
    {"problem": "17 × 24", "claim": "17 × 24 = 418", "condition_holds": True},
    {"problem": "144 ÷ 12", "claim": "144 ÷ 12 = 14", "condition_holds": True},
    {"problem": "(8 + 4) × 3", "claim": "(8 + 4) × 3 = 32", "condition_holds": True},
]

math_requests = [
    {"prompt": "What is {problem}?", "expected_response_type": "answer", "tags": Tags(domain="math", form="question", wording="standard")},
    {"prompt": "what is {problem}", "expected_response_type": "answer", "tags": Tags(domain="math", form="question", wording="nonstandard")},
    {"prompt": "Can you solve {problem}?", "expected_response_type": "answer", "tags": Tags(domain="math", form="question", wording="standard")},
    {
        "prompt": [
            {"role": "user", "content": "Here is a problem: {problem}"},
            {"role": "assistant", "content": "What would you like me to do?"},
            {"role": "user", "content": "can you solve it"},
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="math", form="question", wording="nonstandard"),
    },
    {"prompt": "Is this correct: {claim}?", "expected_response_type": "answer", "tags": Tags(domain="math", form="question", wording="standard")},
    {"prompt": "is this correct {claim}", "expected_response_type": "answer", "tags": Tags(domain="math", form="question", wording="nonstandard")},
    {"prompt": "Solve {problem}.", "expected_response_type": "executed", "tags": Tags(domain="math", form="delegation", wording="standard")},
    {"prompt": "solve {problem}", "expected_response_type": "executed", "tags": Tags(domain="math", form="delegation", wording="nonstandard")},
    {"prompt": "If the claim ‘{claim}’ is incorrect, solve {problem}.", "expected_response_type": "answer", "tags": Tags(domain="math", form="conditional", wording="standard")},
    {"prompt": "if the claim {claim} is incorrect solve {problem}", "expected_response_type": "answer", "tags": Tags(domain="math", form="conditional", wording="nonstandard")},
]

grammar_problems = [
    {"problem": "She go home every day.", "claim": "She goes home every day.", "condition_holds": False},
    {"problem": "The build passed, we deployed it.", "claim": "The build passed, so we deployed it.", "condition_holds": False},
    {"problem": "The three developer's laptops were updated.", "claim": "The three developers' laptops were updated.", "condition_holds": False},
    {"problem": "She go home every day.", "claim": "She going home every day.", "condition_holds": True},
    {"problem": "The build passed, we deployed it.", "claim": "The build passed so, we deployed it.", "condition_holds": True},
    {"problem": "The three developer's laptops were updated.", "claim": "The three developers laptop's were updated.", "condition_holds": True},
]

grammar_requests = [
    {"prompt": "What is wrong with this sentence?\n\n{problem}", "expected_response_type": "answer", "tags": Tags(domain="grammar", form="question", wording="standard")},
    {"prompt": "whats wrong with this sentence\n\n{problem}", "expected_response_type": "answer", "tags": Tags(domain="grammar", form="question", wording="nonstandard")},
    {"prompt": "Can you correct this sentence?\n\n{problem}", "expected_response_type": "answer", "tags": Tags(domain="grammar", form="question", wording="standard")},
    {
        "prompt": [
            {"role": "user", "content": "Here is a sentence:\n\n{problem}"},
            {"role": "assistant", "content": "What should I do with it?"},
            {"role": "user", "content": "can you correct it"},
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="grammar", form="question", wording="nonstandard"),
    },
    {"prompt": "Is the proposed revision correct?\n\nOriginal:\n{problem}\n\nProposed revision:\n{claim}", "expected_response_type": "answer", "tags": Tags(domain="grammar", form="question", wording="standard")},
    {"prompt": "is the proposed revision correct\n\noriginal\n{problem}\n\nproposed revision\n{claim}", "expected_response_type": "answer", "tags": Tags(domain="grammar", form="question", wording="nonstandard")},
    {"prompt": "Correct this sentence.\n\n{problem}", "expected_response_type": "executed", "tags": Tags(domain="grammar", form="delegation", wording="standard")},
    {"prompt": "correct this sentence\n\n{problem}", "expected_response_type": "executed", "tags": Tags(domain="grammar", form="delegation", wording="nonstandard")},
    {"prompt": "Is the proposed revision correct? Then correct the original sentence.\n\nOriginal:\n{problem}\n\nProposed revision:\n{claim}", "expected_response_type": "answer_then_execution", "tags": Tags(domain="grammar", form="mixed", wording="standard")},
    {"prompt": "is the proposed revision correct then correct the original sentence\n\noriginal\n{problem}\n\nproposed revision\n{claim}", "expected_response_type": "answer_then_execution", "tags": Tags(domain="grammar", form="mixed", wording="nonstandard")},
    {"prompt": "Correct the original sentence. Then say whether the proposed revision is valid.\n\nOriginal:\n{problem}\n\nProposed revision:\n{claim}", "expected_response_type": "execution_then_answer", "tags": Tags(domain="grammar", form="mixed", wording="standard")},
    {"prompt": "correct the original sentence then say whether the proposed revision is valid\n\noriginal\n{problem}\n\nproposed revision\n{claim}", "expected_response_type": "execution_then_answer", "tags": Tags(domain="grammar", form="mixed", wording="nonstandard")},
    {"prompt": "If the proposed revision is invalid, correct the original sentence.\n\nOriginal:\n{problem}\n\nProposed revision:\n{claim}", "expected_response_type": "answer", "tags": Tags(domain="grammar", form="conditional", wording="standard")},
    {"prompt": "if the proposed revision is invalid correct the original sentence\n\noriginal\n{problem}\n\nproposed revision\n{claim}", "expected_response_type": "answer", "tags": Tags(domain="grammar", form="conditional", wording="nonstandard")},
]

code_problems = [
    {"problem": """def last(items):
    return items[len(items)]""", "claim": """def last(items):
    return items[-1]""", "condition_holds": False},
    {"problem": """def is_even(value):
    return value % 2 == 1""", "claim": """def is_even(value):
    return value % 2 == 0""", "condition_holds": False},
    {"problem": """def add(left, right):
    return left - right""", "claim": """def add(left, right):
    return left + right""", "condition_holds": False},
    {"problem": """def last(items):
    return items[len(items)]""", "claim": """def last(items):
    return items[len(items) + 1]""", "condition_holds": True},
    {"problem": """def is_even(value):
    return value % 2 == 1""", "claim": """def is_even(value):
    return value % 2 != 0""", "condition_holds": True},
    {"problem": """def add(left, right):
    return left - right""", "claim": """def add(left, right):
    return right - left""", "condition_holds": True},
]

code_requests = [
    {"prompt": "What’s the bug in this code?\n\n```python\n{problem}\n```", "expected_response_type": "answer", "tags": Tags(domain="code", form="question", wording="standard")},
    {"prompt": "whats the bug in this code\n\n```python\n{problem}\n```", "expected_response_type": "answer", "tags": Tags(domain="code", form="question", wording="nonstandard")},
    {"prompt": "Can you fix the bug in this code?\n\n```python\n{problem}\n```", "expected_response_type": "answer", "tags": Tags(domain="code", form="question", wording="standard")},
    {
        "prompt": [
            {"role": "user", "content": "Here is some code:\n\n```python\n{problem}\n```"},
            {"role": "assistant", "content": "What should I do with it?"},
            {"role": "user", "content": "can you fix the bug"},
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="code", form="question", wording="nonstandard"),
    },
    {"prompt": "Does the proposed revision fix the bug?\n\nOriginal:\n```python\n{problem}\n```\n\nProposed revision:\n```python\n{claim}\n```", "expected_response_type": "answer", "tags": Tags(domain="code", form="question", wording="standard")},
    {"prompt": "does the proposed revision fix the bug\n\noriginal\n```python\n{problem}\n```\n\nproposed revision\n```python\n{claim}\n```", "expected_response_type": "answer", "tags": Tags(domain="code", form="question", wording="nonstandard")},
    {"prompt": "Fix the bug in this code.\n\n```python\n{problem}\n```", "expected_response_type": "executed", "tags": Tags(domain="code", form="delegation", wording="standard")},
    {"prompt": "fix the bug in this code\n\n```python\n{problem}\n```", "expected_response_type": "executed", "tags": Tags(domain="code", form="delegation", wording="nonstandard")},
    {"prompt": "Does the proposed revision fix the bug? Then fix the bug.\n\nOriginal:\n```python\n{problem}\n```\n\nProposed revision:\n```python\n{claim}\n```", "expected_response_type": "answer_then_execution", "tags": Tags(domain="code", form="mixed", wording="standard")},
    {"prompt": "does the proposed revision fix the bug then fix the bug\n\noriginal\n```python\n{problem}\n```\n\nproposed revision\n```python\n{claim}\n```", "expected_response_type": "answer_then_execution", "tags": Tags(domain="code", form="mixed", wording="nonstandard")},
    {"prompt": "Fix the bug. Then say whether the proposed revision fixes it.\n\nOriginal:\n```python\n{problem}\n```\n\nProposed revision:\n```python\n{claim}\n```", "expected_response_type": "execution_then_answer", "tags": Tags(domain="code", form="mixed", wording="standard")},
    {"prompt": "fix the bug then say whether the proposed revision fixes it\n\noriginal\n```python\n{problem}\n```\n\nproposed revision\n```python\n{claim}\n```", "expected_response_type": "execution_then_answer", "tags": Tags(domain="code", form="mixed", wording="nonstandard")},
    {"prompt": "If the proposed revision does not fix the bug, fix it.\n\nOriginal:\n```python\n{problem}\n```\n\nProposed revision:\n```python\n{claim}\n```", "expected_response_type": "answer", "tags": Tags(domain="code", form="conditional", wording="standard")},
    {"prompt": "if the proposed revision does not fix the bug fix it\n\noriginal\n```python\n{problem}\n```\n\nproposed revision\n```python\n{claim}\n```", "expected_response_type": "answer", "tags": Tags(domain="code", form="conditional", wording="nonstandard")},
]


examples = [
    {
        "prompt": (
            request["prompt"].format(**problem)
            if isinstance(request["prompt"], str)
            else [
                {**message, "content": message["content"].format(**problem)}
                for message in request["prompt"]
            ]
        ),
        "expected_response_type": (
            "executed"
            if problem["condition_holds"] and request["tags"]["form"] == "conditional"
            else request["expected_response_type"]
        ),
        "tags": request["tags"],
    }
    for problems, requests in (
        (math_problems, math_requests),
        (grammar_problems, grammar_requests),
        (code_problems, code_requests),
    )
    for problem in problems
    for request in requests
    if not problem["condition_holds"]
    or (
        request["tags"]["form"] in {"question", "conditional"}
        and "{claim}" in str(request["prompt"])
    )
]
