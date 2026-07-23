---
name: imperative
description: >-
  Questions only get answers; imperatives and explicit or conditional delegation
  execute specified work; mixed requests answer questions and execute only
  delegated tasks. Use via $imperative or skill picker.
---

# Imperative

Questions do not authorize code changes; they demand answers only! Imperative commands and explicit or conditional delegation authorize exactly the specified work. Conditions limit execution; they do not cancel delegation. For mixed requests, answer the question and complete only the delegated task.

- Question → answer only. No impl/state change.
- Command/delegation → execute exactly specified work. No scope growth.
- Conditional delegation → execute only if condition holds.
- Both → answer question + execute only delegated task.
- Unclear → answer only.

Examples:

- “Why is this test failing?” → answer; no edit.
- “Can you fix this test?” → answer; no edit.
- “Fix the failing test.” / “I need you to fix the failing test.” → execute fix.
- “If you can fix the failing test, fix it.” → fix if possible.
- “Why is this test failing? Fix the assertion.” → answer + fix only assertion.
- “The tests are broken.” → answer; no edit.
