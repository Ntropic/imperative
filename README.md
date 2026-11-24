# Imperative

**Answer what’s asked. Change what’s requested.**

Imperative is a skill for coding agents.

| Model | Score |
| --- | ---: |
| Inkling 2 Mini | 169/171 (98.8%) |
| GPT-6.2 Sol (low reasoning) | 171/171 (100%) |

- **Questions**
  - Answer directly. Include a brief inline correction when it helps.
  - Keep yes/no answers short, including questions about what the agent can do.
- **Requests**
  - Carry out explicit requests within the scope the user authorized.
  - Ask for consent before departing from an agreed scope or plan.
- **Conditional requests**
  - Check the condition first. Carry out the requested work only if it holds.
- **Change of mind**
  - Apply the latest instruction to any question, request, or condition it changes. If instructions conflict, follow the last one on that point, even within one message. Stop canceled work.

## Install

Run from the project where you’ll use Imperative.

```bash
npx skills add https://github.com/Ntropic/imperative --skill imperative
```

Select or mention **Imperative** in your agent. Add `--global` to install it across projects. [skills.sh directory](https://skills.sh/)

## Examples

| Prompt | Behavior |
|---|---|
| “Why is this test failing?” | Explain the cause. |
| “What would the patch look like?” | Show the patch in chat. |
| “Fix this test.” | Apply and verify the fix. |
| “If the test fails, fix it.” | Check first. Fix it only if it fails. |
| “Fix it. Actually, hold off. What’s wrong?” | Explain the cause. Leave the files alone. |

[`SKILL.md`](skills/imperative/SKILL.md) · [Text evaluator and 171 test cases](skilltester/README.md)
