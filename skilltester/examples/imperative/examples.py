# Exports: system_prompt, response_types, optional Tags, and examples like {"prompt": ..., "expected_response_type": ..., "tags": ...}.

from typing import Literal, TypedDict


system_prompt = "You are a helpful assistant. Respond directly and accurately."

response_types = {
    "answer": (
        "Gave information without carrying out the action under discussion. "
        "Answering a direct information question, answering only whether an action is possible, "
        "or reporting that a condition is false all count as answers without execution. "
        "A requested result, corrected wording, derivation, or code sample in chat counts as "
        "answering the question, including when the user says 'Can you tell me' or 'Can you show me'. "
        "A bare number is an answer when the latest message asks for the result of a calculation, "
        "including when the expression appeared in an earlier message. "
        "A brief inline correction, calculation, or replacement line that directly supports "
        "a diagnosis also counts as part of the answer. "
        "Evidence used to check a condition is distinct from the deliverable gated by that condition."
    ),
    "executed": (
        "Carried out the action without separately answering a question. "
        "For a task done in chat, delivering the requested result counts as execution. "
        "For example, '56' answers 'What is 7 × 8?' and executes 'Solve 7 × 8.' "
        "For a capability question about producing a separate deliverable, such as a full script "
        "or document, producing that deliverable counts as execution. "
        "A standalone rewrite, patch, or regression test supplied beyond what a diagnostic question "
        "asks counts as execution, including when the user withdrew that earlier task. "
        "Explaining a condition check or an edit as part of the requested work does not count "
        "as a separate answer."
    ),
    "answer_then_execution": (
        "First gave a substantive answer to a separate question, then delivered the action's result. "
        "Count a condition check as a separate answer only if the user separately asked about it. "
        "Use the order in the candidate's reply, even if it differs from the requested order."
    ),
    "execution_then_answer": (
        "First delivered the action's result, then gave a substantive answer to a separate question. "
        "An instruction such as 'say whether the proposed revision is valid' requests an answer. "
        "An explicit assessment such as 'the proposed revision is valid' answers it."
    ),
}


class PromptTags(TypedDict):
    domain: Literal["math", "grammar", "code"]
    form: Literal["question", "delegation", "conditional", "mixed", "change_of_mind"]
    wording: Literal["standard", "nonstandard"]


class Tags(PromptTags):
    difficulty: Literal["easy", "hard"]


math_problems = [
    {"problem": "17 × 24", "claim": "17 × 24 = 408", "condition_holds": False},
    {"problem": "144 ÷ 12", "claim": "144 ÷ 12 = 12", "condition_holds": False},
    {"problem": "(8 + 4) × 3", "claim": "(8 + 4) × 3 = 36", "condition_holds": False},
    {"problem": "17 × 24", "claim": "17 × 24 = 418", "condition_holds": True},
    {"problem": "144 ÷ 12", "claim": "144 ÷ 12 = 14", "condition_holds": True},
    {"problem": "(8 + 4) × 3", "claim": "(8 + 4) × 3 = 32", "condition_holds": True},
]

math_requests = [
    {"prompt": "What is {problem}?", "expected_response_type": "answer", "tags": PromptTags(domain="math", form="question", wording="standard")},
    {"prompt": "what is {problem}", "expected_response_type": "answer", "tags": PromptTags(domain="math", form="question", wording="nonstandard")},
    {"prompt": "Can you tell me the result of {problem}?", "expected_response_type": "answer", "tags": PromptTags(domain="math", form="question", wording="standard")},
    {
        "prompt": [
            {"role": "user", "content": "Here is a problem: {problem}"},
            {"role": "assistant", "content": "What would you like me to do?"},
            {"role": "user", "content": "can you tell me the result"},
        ],
        "expected_response_type": "answer",
        "tags": PromptTags(domain="math", form="question", wording="nonstandard"),
    },
    {"prompt": "Is this correct: {claim}?", "expected_response_type": "answer", "tags": PromptTags(domain="math", form="question", wording="standard")},
    {"prompt": "is this correct {claim}", "expected_response_type": "answer", "tags": PromptTags(domain="math", form="question", wording="nonstandard")},
    {"prompt": "Solve {problem}.", "expected_response_type": "executed", "tags": PromptTags(domain="math", form="delegation", wording="standard")},
    {"prompt": "solve {problem}", "expected_response_type": "executed", "tags": PromptTags(domain="math", form="delegation", wording="nonstandard")},
    {"prompt": "If the claim ‘{claim}’ is incorrect, give twice the correct result.", "expected_response_type": "answer", "tags": PromptTags(domain="math", form="conditional", wording="standard")},
    {"prompt": "if the claim {claim} is incorrect give twice the correct result", "expected_response_type": "answer", "tags": PromptTags(domain="math", form="conditional", wording="nonstandard")},
]

grammar_problems = [
    {"problem": "She go home every day.", "claim": "She goes home every day.", "condition_holds": False},
    {"problem": "The build passed, we deployed it.", "claim": "The build passed, and we deployed it.", "condition_holds": False},
    {"problem": "The three developer's laptops were updated.", "claim": "The three developers' laptops were updated.", "condition_holds": False},
    {"problem": "She go home every day.", "claim": "She going home every day.", "condition_holds": True},
    {"problem": "The build passed, we deployed it.", "claim": "The build passed so, we deployed it.", "condition_holds": True},
    {"problem": "The three developer's laptops were updated.", "claim": "The three developers laptop's were updated.", "condition_holds": True},
]

grammar_requests = [
    {"prompt": "What is wrong with this sentence?\n\n{problem}", "expected_response_type": "answer", "tags": PromptTags(domain="grammar", form="question", wording="standard")},
    {"prompt": "whats wrong with this sentence\n\n{problem}", "expected_response_type": "answer", "tags": PromptTags(domain="grammar", form="question", wording="nonstandard")},
    {"prompt": "Can you tell me the corrected wording of this sentence?\n\n{problem}", "expected_response_type": "answer", "tags": PromptTags(domain="grammar", form="question", wording="standard")},
    {
        "prompt": [
            {"role": "user", "content": "Here is a sentence:\n\n{problem}"},
            {"role": "assistant", "content": "What should I do with it?"},
            {"role": "user", "content": "can you show me the corrected sentence"},
        ],
        "expected_response_type": "answer",
        "tags": PromptTags(domain="grammar", form="question", wording="nonstandard"),
    },
    {"prompt": "Is the proposed revision correct?\n\nOriginal:\n{problem}\n\nProposed revision:\n{claim}", "expected_response_type": "answer", "tags": PromptTags(domain="grammar", form="question", wording="standard")},
    {"prompt": "is the proposed revision correct\n\noriginal\n{problem}\n\nproposed revision\n{claim}", "expected_response_type": "answer", "tags": PromptTags(domain="grammar", form="question", wording="nonstandard")},
    {"prompt": "Correct this sentence.\n\n{problem}", "expected_response_type": "executed", "tags": PromptTags(domain="grammar", form="delegation", wording="standard")},
    {"prompt": "correct this sentence\n\n{problem}", "expected_response_type": "executed", "tags": PromptTags(domain="grammar", form="delegation", wording="nonstandard")},
    {"prompt": "Is the proposed revision correct? Then correct the original sentence.\n\nOriginal:\n{problem}\n\nProposed revision:\n{claim}", "expected_response_type": "answer_then_execution", "tags": PromptTags(domain="grammar", form="mixed", wording="standard")},
    {"prompt": "is the proposed revision correct then correct the original sentence\n\noriginal\n{problem}\n\nproposed revision\n{claim}", "expected_response_type": "answer_then_execution", "tags": PromptTags(domain="grammar", form="mixed", wording="nonstandard")},
    {"prompt": "Correct the original sentence. Then say whether the proposed revision is valid.\n\nOriginal:\n{problem}\n\nProposed revision:\n{claim}", "expected_response_type": "execution_then_answer", "tags": PromptTags(domain="grammar", form="mixed", wording="standard")},
    {"prompt": "correct the original sentence then say whether the proposed revision is valid\n\noriginal\n{problem}\n\nproposed revision\n{claim}", "expected_response_type": "execution_then_answer", "tags": PromptTags(domain="grammar", form="mixed", wording="nonstandard")},
    {"prompt": "If the proposed revision is invalid, translate the intended meaning of the original sentence into Spanish.\n\nOriginal:\n{problem}\n\nProposed revision:\n{claim}", "expected_response_type": "answer", "tags": PromptTags(domain="grammar", form="conditional", wording="standard")},
    {"prompt": "if the proposed revision is invalid translate the original sentence's intended meaning into spanish\n\noriginal\n{problem}\n\nproposed revision\n{claim}", "expected_response_type": "answer", "tags": PromptTags(domain="grammar", form="conditional", wording="nonstandard")},
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
    {"prompt": "What’s the bug in this code?\n\n```python\n{problem}\n```", "expected_response_type": "answer", "tags": PromptTags(domain="code", form="question", wording="standard")},
    {"prompt": "whats the bug in this code\n\n```python\n{problem}\n```", "expected_response_type": "answer", "tags": PromptTags(domain="code", form="question", wording="nonstandard")},
    {"prompt": "Can you show me the one line that would fix the bug?\n\n```python\n{problem}\n```", "expected_response_type": "answer", "tags": PromptTags(domain="code", form="question", wording="standard")},
    {
        "prompt": [
            {"role": "user", "content": "Here is some code:\n\n```python\n{problem}\n```"},
            {"role": "assistant", "content": "What should I do with it?"},
            {"role": "user", "content": "can you tell me what's wrong and show the replacement line"},
        ],
        "expected_response_type": "answer",
        "tags": PromptTags(domain="code", form="question", wording="nonstandard"),
    },
    {"prompt": "Does the proposed revision fix the bug?\n\nOriginal:\n```python\n{problem}\n```\n\nProposed revision:\n```python\n{claim}\n```", "expected_response_type": "answer", "tags": PromptTags(domain="code", form="question", wording="standard")},
    {"prompt": "does the proposed revision fix the bug\n\noriginal\n```python\n{problem}\n```\n\nproposed revision\n```python\n{claim}\n```", "expected_response_type": "answer", "tags": PromptTags(domain="code", form="question", wording="nonstandard")},
    {"prompt": "Fix the bug in this code.\n\n```python\n{problem}\n```", "expected_response_type": "executed", "tags": PromptTags(domain="code", form="delegation", wording="standard")},
    {"prompt": "fix the bug in this code\n\n```python\n{problem}\n```", "expected_response_type": "executed", "tags": PromptTags(domain="code", form="delegation", wording="nonstandard")},
    {"prompt": "Does the proposed revision fix the bug? Then fix the bug.\n\nOriginal:\n```python\n{problem}\n```\n\nProposed revision:\n```python\n{claim}\n```", "expected_response_type": "answer_then_execution", "tags": PromptTags(domain="code", form="mixed", wording="standard")},
    {"prompt": "does the proposed revision fix the bug then fix the bug\n\noriginal\n```python\n{problem}\n```\n\nproposed revision\n```python\n{claim}\n```", "expected_response_type": "answer_then_execution", "tags": PromptTags(domain="code", form="mixed", wording="nonstandard")},
    {"prompt": "Fix the bug. Then say whether the proposed revision fixes it.\n\nOriginal:\n```python\n{problem}\n```\n\nProposed revision:\n```python\n{claim}\n```", "expected_response_type": "execution_then_answer", "tags": PromptTags(domain="code", form="mixed", wording="standard")},
    {"prompt": "fix the bug then say whether the proposed revision fixes it\n\noriginal\n```python\n{problem}\n```\n\nproposed revision\n```python\n{claim}\n```", "expected_response_type": "execution_then_answer", "tags": PromptTags(domain="code", form="mixed", wording="nonstandard")},
    {"prompt": "If the proposed revision does not fix the bug, write a regression test that fails on the proposed revision.\n\nOriginal:\n```python\n{problem}\n```\n\nProposed revision:\n```python\n{claim}\n```", "expected_response_type": "answer", "tags": PromptTags(domain="code", form="conditional", wording="standard")},
    {"prompt": "if the proposed revision does not fix the bug write a regression test that fails on the proposed revision\n\noriginal\n```python\n{problem}\n```\n\nproposed revision\n```python\n{claim}\n```", "expected_response_type": "answer", "tags": PromptTags(domain="code", form="conditional", wording="nonstandard")},
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
        "tags": {**request["tags"], "difficulty": "easy"},
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

examples += [
    {
        "prompt": (
            "I'm assembling a worksheet for a group that hasn't learned fractions yet. It uses three "
            "rows of totals and a small box at the bottom for an everyday example. A colleague asked "
            "whether a second version would help students who miss the first lesson. Before I decide, "
            "are you able to draft a second worksheet with a worked example and four practice problems?"
        ),
        "expected_response_type": "answer",
        "tags": Tags(domain="math", form="question", wording="standard", difficulty="hard"),
    },
    {
        "prompt": (
            "This sentence is from a training note for new staff: 'The list of required checks are "
            "on the first page.' The printer has already set the page, so any comment will go in our "
            "review log. The subject is supposed to be the list itself. What's grammatically wrong "
            "with the sentence?"
        ),
        "expected_response_type": "answer",
        "tags": Tags(domain="grammar", form="question", wording="standard", difficulty="hard"),
    },
    {
        "prompt": (
            "We're documenting the handoff between support and fulfillment. The audience already "
            "knows where to find the order number. Our draft says, 'You gotta send the order number "
            "before we can check the shipment.' Rewrite that sentence in a neutral, professional tone "
            "and preserve the requirement to send the number first."
        ),
        "expected_response_type": "executed",
        "tags": Tags(domain="grammar", form="delegation", wording="standard", difficulty="hard"),
    },
    {
        "prompt": (
            "The inventory sheet lists 23 boxes in each of 14 crates. The printed total is 322. "
            "The supervisor only wants a new label when the printed total is wrong. If 322 is "
            "incorrect, draft a replacement shipping label with the correct total and a space "
            "for the supervisor's initials."
        ),
        "expected_response_type": "answer",
        "tags": Tags(domain="math", form="conditional", wording="standard", difficulty="hard"),
    },
    {
        "prompt": (
            "This helper drops the oldest event from a list ordered from oldest to newest. The author "
            "proposed `return events[:-1]` inside `drop_oldest(events)`. Batch processing uses this "
            "helper, but single-event batches are tested elsewhere. If the proposed slice drops the "
            "wrong end, write one regression test with at least two distinct events."
        ),
        "expected_response_type": "executed",
        "tags": Tags(domain="code", form="conditional", wording="standard", difficulty="hard"),
    },
    {
        "prompt": (
            "I'm reconciling a small inventory sheet. There are 18 sealed cartons with 12 pieces each "
            "and an opened carton with 7 pieces. The packing slip claims 230 pieces. First say whether "
            "that claim is correct. Then produce a one-line inventory entry with the total and the "
            "number of sealed cartons."
        ),
        "expected_response_type": "answer_then_execution",
        "tags": Tags(domain="math", form="mixed", wording="standard", difficulty="hard"),
    },
    {
        "prompt": (
            "Make a worked solution and three practice questions for 84 divided by 7. Actually, "
            "hold off on writing any material. I'm deciding whether to use it for a lesson on "
            "remainders and just need to know whether 84 is divisible by 7."
        ),
        "expected_response_type": "answer",
        "tags": Tags(domain="math", form="change_of_mind", wording="standard", difficulty="hard"),
    },
    {
        "prompt": [
            {"role": "user", "content": "When I send the figures, make a budget table with one row for materials and one for labor."},
            {"role": "assistant", "content": "Send the figures when you have them."},
            {
                "role": "user",
                "content": (
                    "Materials are 85 and labor is 140. I looked at the finance template again, and "
                    "we already have a table. Drop the table request. What's the combined total?"
                ),
            },
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="math", form="change_of_mind", wording="standard", difficulty="hard"),
    },
    {
        "prompt": [
            {"role": "user", "content": "When I send the dimensions, draft a printable floor-plan label with a title, the dimensions, and the area."},
            {"role": "assistant", "content": "What dimensions should I use?"},
            {
                "role": "user",
                "content": (
                    "7.5 m by 4 m. Cancel the label. The project lead only asked for the area. "
                    "What's the area in square metres?"
                ),
            },
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="math", form="change_of_mind", wording="standard", difficulty="hard"),
    },
    {
        "prompt": (
            "Please rewrite 'The boxes was stored outside' in the same tone as the rest of our "
            "inventory sheet. actually wait, i need to give the writer feedback first. what's "
            "the grammatical issue? leave the wording as it is for now"
        ),
        "expected_response_type": "answer",
        "tags": Tags(domain="grammar", form="change_of_mind", wording="nonstandard", difficulty="hard"),
    },
    {
        "prompt": [
            {"role": "user", "content": "When I paste the line, rewrite it in a warmer tone and translate it into French."},
            {"role": "assistant", "content": "Please send the line."},
            {
                "role": "user",
                "content": (
                    "The line is 'You failed to send the invoice on time.' I've changed my mind. "
                    "I need neither new copy nor a translation. Does the line sound accusatory, and "
                    "which words contribute most to that impression?"
                ),
            },
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="grammar", form="change_of_mind", wording="standard", difficulty="hard"),
    },
    {
        "prompt": [
            {"role": "user", "content": "When I send the copy, replace it with a professional version suitable for a customer email."},
            {"role": "assistant", "content": "Send the copy whenever you're ready."},
            {
                "role": "user",
                "content": (
                    "Here it is: 'The package got here yesterday and it was open.' Leave it in "
                    "the sender's words. Instead of rewriting it, tell me whether the line "
                    "identifies who opened the package."
                ),
            },
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="grammar", form="change_of_mind", wording="standard", difficulty="hard"),
    },
    {
        "prompt": (
            "Fix the implementation and add a regression test for the issue below. Actually, pause "
            "both changes while I check whether the caller relies on the current behavior. For now, "
            "what does `difference(9, 4)` return, and why?\n\n"
            "```python\ndef difference(left, right):\n    return right - left\n```"
        ),
        "expected_response_type": "answer",
        "tags": Tags(domain="code", form="change_of_mind", wording="standard", difficulty="hard"),
    },
    {
        "prompt": [
            {"role": "user", "content": "When I send the function, rewrite it to handle empty lists and add a test."},
            {"role": "assistant", "content": "Share the function so I can see how it currently works."},
            {
                "role": "user",
                "content": (
                    "Hold off on both changes. We need to document the old behavior for callers "
                    "that may depend on it. What happens when this function receives an empty list?\n\n"
                    "```python\ndef first_or_none(items):\n    return items[0]\n```"
                ),
            },
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="code", form="change_of_mind", wording="standard", difficulty="hard"),
    },
    {
        "prompt": [
            {"role": "user", "content": "Please produce a patched version when I send the code."},
            {"role": "assistant", "content": "Share the code when you're ready."},
            {
                "role": "user",
                "content": (
                    "let's leave the implementation alone for this review. i only want to know if "
                    "the helper removes duplicates while preserving order. the callers expect a list, "
                    "and their inputs can include the same value more than once.\n\n"
                    "```python\ndef unique(values):\n    return list(set(values))\n```"
                ),
            },
        ],
        "expected_response_type": "answer",
        "tags": Tags(domain="code", form="change_of_mind", wording="nonstandard", difficulty="hard"),
    },
]

artifact_cases = [
    (
        "code",
        "Our operations team receives two CSV files named invoices.csv and payments.csv. "
        "Both have an invoice_id column. We need a standalone Python command-line script "
        "that joins the files, reports unmatched IDs and differing amounts, and exits "
        "with a nonzero code when it finds discrepancies.",
        "write the reconciliation script",
        "reconciliation script",
    ),
    (
        "grammar",
        "We're onboarding support staff to a new returns workflow. Agents check the order "
        "number, verify that the purchase is within 30 days, and escalate damaged or "
        "international returns. We need a complete internal guide with a decision table "
        "and a worked example of an escalation.",
        "draft the returns guide",
        "returns guide",
    ),
]

examples += [
    {
        "prompt": f"{context}\n\n{request}",
        "expected_response_type": expected_response_type,
        "tags": Tags(domain=domain, form=form, wording="standard", difficulty="hard"),
    }
    for domain, context, task, artifact in artifact_cases
    for request, expected_response_type, form in (
        (f"Can you {task}?", "answer", "question"),
        (f"Can you show me the complete {artifact} here in chat?", "answer", "question"),
        (f"Please {task}. Include the complete result in chat.", "executed", "delegation"),
    )
]
