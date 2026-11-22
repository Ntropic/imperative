# Imperative

**Answer what’s asked. Change what’s requested.**

Agents confuse questions with permission. Ask why; get an edit. Request one fix; get a cleanup spree.

Models are trained and showcased on impressive single-shot prototypes. Incomplete prompts reward them for inferring unstated product and implementation decisions. That looks powerful in a demo, but quietly substitutes model judgment for user authorization.

Imperative minimizes that inference: questions get answers, requests grant scoped authority, and material course changes require fresh consent.

## Install

```bash
npx skills add ntropic/imperative --skill imperative
```

The installer detects Claude Code, Codex, Gemini CLI, GitHub Copilot, and other compatible agents. Add `--global` for all projects.

## Use

```text
/imperative [request]
```

**Answers, not actions, follow from questions.** Execute only explicit requests.

## Examples

| Request | Result |
|---|---|
| “Why is this failing?” | Answer. No edit. |
| “Can you fix this?” | Answer. No edit. |
| “Fix this.” | Fix it. |
| “If the test fails, fix it.” | Test; fix only if failing. |
| “What version is installed? Update it.” | Answer first; then update. |

## Tests

- Skill validation: **passed**
- Python evaluator dry-run: **126 runs generated; 0 errors**
- Local model evaluator retained outside Git

Core skill: [`skills/imperative/SKILL.md`](skills/imperative/SKILL.md)
