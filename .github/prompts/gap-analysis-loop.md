---
title: "Gap Analysis Loop"
description: "Systematically identify, track, and resolve knowledge gaps through iterative investigation passes, maintaining a live gap register between passes."
intent-tags: [gap-analysis, research]
modes: ["deep-researcher"]
output-format: "enumerated gap list"
when-to-use: "At the start of any research session and after each search pass. Use to govern the iterative research loop — each pass must begin by selecting from the gap register and end by updating it."
---

# Gap Analysis Loop Protocol

## Purpose

Prevent research from being breadth-first (searching everything broadly) or depth-first (drilling one thread
to exhaustion). Instead, maintain a live register of what is unknown and systematically close gaps in
priority order.

## Gap Register Format

```
## Gap Register — {Topic}

### OPEN
- [ ] GAP-{N}: {What is unknown, stated as a question} [Priority: HIGH/MED/LOW]

### CLOSED
- [x] GAP-{N}: {Original question} → {Answer in one sentence} [Source: {URL or ref}]

### INVALIDATED
- [-] GAP-{N}: {Original question} → {Why this turned out not to matter}
```

## Loop Execution

### Before Pass 1 — Seed the Register

From the research question and any prior memory context, enumerate every significant unknown.
Ask: "If I knew nothing else, what would prevent me from answering the research question?"
Each answer becomes a GAP entry. Minimum 3 gaps to start a research session.

### Each Pass — Single Gap Focus

1. Select the highest-priority OPEN gap
2. State which gap you are targeting before searching
3. Execute 1–3 targeted searches for that specific gap
4. On finding an answer: close the gap, record the source
5. On surfacing new unknowns: add them to OPEN immediately
6. On finding the gap is moot: move to INVALIDATED with reasoning
7. Present the updated register after every pass — no silent passes

### Stop Conditions (evaluate after every pass)

- All gaps CLOSED or INVALIDATED → proceed to synthesis
- Pass yielded zero new findings AND zero new gaps → diminishing returns → proceed to synthesis
- Pass count reaches 5 → hard stop → proceed to synthesis, list remaining OPEN gaps as "Remaining Open Questions"
- User says "enough" / "stop" → proceed to synthesis immediately

## Gap Priority Rules

- **HIGH:** gap whose answer would change the overall conclusion
- **MED:** gap that adds important nuance but won't change the conclusion
- **LOW:** gap that is interesting but not decision-relevant — deprioritise; may remain open

## Quality Gate

After each pass, verify: "Is every OPEN gap genuinely unknown, or am I deferring something I already know?"
Deferred known facts should be CLOSED immediately — not kept open to pad the register.
