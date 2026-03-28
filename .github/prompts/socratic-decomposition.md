---
title: "Socratic Decomposition"
description: "Resolve ambiguous or underspecified requests through targeted questioning that systematically narrows the solution space until one clear path emerges."
intent-tags: [decompose, socratic, ambiguity]
modes: ["all"]
output-format: "clarifying Q&A sequence"
when-to-use: "When a request has multiple valid interpretations, unstated constraints, unclear success criteria, or conflicting signals. Use before planning, not during implementation."
---

# Socratic Decomposition Protocol

For deeper treatment, see `.github/exploits/socratic-questioning.md`. This prompt is the condensed, agent-executable pattern.

## When to Apply

- ≥2 reasonable interpretations with meaningfully different outcomes
- Success criteria undefined ("make it better", "add validation")
- Requirements contradict each other or the codebase
- Request implies an unresolved architectural choice

## Do NOT Apply When

- A single obvious interpretation exists — just act
- Request is specific and complete

## Execution Pattern

**Step 1: Classify the ambiguity**
- **Scope** — unclear boundaries
- **Specification** — undefined success condition
- **Constraint** — unknown hard requirements
- **Trade-off** — unclear user values
- **Architecture** — unresolved structural intent

**Step 2: Ask the minimum viable question**

Max 2 questions per exchange. Format:
```
[CONTEXT: what I understand — 1 sentence]
[QUESTION: specific, bounded]
Option A: {interpretation + consequence}
Option B: {interpretation + consequence}
```

**Step 3: Narrow and confirm**
- State what is now resolved; state what (if anything) remains
- If still ambiguous: one more targeted question
- If resolved: "Confirmed — I'll proceed with: {interpretation}."

## Stop Condition

One clear path with zero blocking unknowns. Questions must be: specific (names options) · actionable (directly informs what gets built) · bounded (multiple choice > open-ended) · minimal.
