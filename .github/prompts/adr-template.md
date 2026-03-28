---
title: "Architecture Decision Record"
description: "Produce a structured Architecture Decision Record (ADR) that captures a design decision, its context, consequences, and alternatives considered."
intent-tags: [architecture, decision-record]
modes: ["strategic-collaborator"]
output-format: "ADR document"
when-to-use: "Whenever a significant architectural or design decision has been made or is being evaluated. Minimum 2 alternatives must be considered — if none were, the decision is premature."
---

# Architecture Decision Record Template

## ADR Numbering

ADRs are numbered sequentially per project, starting at ADR-001.
Check `tempo.memory` for prior ADRs on this project before assigning a number.
Never reuse a number, even if a prior ADR is deprecated.

## Mandatory Fields — None Optional

```
# ADR-{NNN}: {The decision, stated as a directive in present tense}
# Example: "ADR-001: Use PostgreSQL as the primary data store"
# Not: "Should we use PostgreSQL?" or "PostgreSQL vs MySQL"

**Status:** Proposed
**Date:** {YYYY-MM-DD}
**Deciders:** {Human name(s) only — the AI proposes, humans decide. AI is never listed here.}

## Context
{2–4 sentences. What forces, constraints, or requirements created the need for this decision?
What is the specific problem this decision resolves?
What would happen if no decision were made?}

## Decision
{1–3 sentences. The decision itself as a clear directive.
"We will use X because Y." Not "X seems like a good fit" or "X is recommended."
The decision must be unambiguous — a new team member reading this should know exactly what was decided.}

## Consequences

### Positive
{Bullet list. What becomes easier, cheaper, faster, or more capable?}

### Negative
{Bullet list. What becomes harder, more constrained, or more expensive?
Be honest — every decision has costs. An ADR with no negative consequences is incomplete.}

### Risks
{Bullet list. What could go wrong? Under what conditions would this decision prove to have been wrong?
Include: reversal cost (how hard is it to undo this decision?)}

## Alternatives Considered
{Minimum 2 alternatives. For each:}

### Alternative: {Name}
**Why rejected:** {One sentence — the specific, honest reason this was not chosen.
Not "it's worse" — state what specific property made it unsuitable for this context.}
```

## Status Lifecycle

- **Proposed:** AI has produced the ADR; human has not yet reviewed
- **Accepted:** Human has reviewed and approved — this is now the decision of record
- **Deprecated:** Decision was accepted but is no longer valid (superseded or context changed)
- **Superseded by ADR-{NNN}:** Explicit successor exists

Only the human changes status from Proposed → Accepted.
The AI sets status to Proposed when producing the ADR. That is all.
