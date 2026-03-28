---
title: "Chain-of-Density Synthesis"
description: "Compress multi-source research findings into a maximally dense, signal-rich brief by iteratively eliminating noise while preserving every essential insight."
intent-tags: [synthesis, research]
modes: ["deep-researcher", "all"]
output-format: "structured brief"
when-to-use: "After completing a research pass or multi-source investigation. Use whenever you need to produce a final output that is dense, actionable, and free of narrative filler."
---

# Chain-of-Density Synthesis Protocol

## Objective

Produce a synthesis brief where every sentence carries signal. Target SNR (Signal-to-Noise Ratio) > 5:1.

**Signal:** decisions, constraints, confirmed findings, sourced facts, risks, dependencies.
**Noise:** hedging language, conversational filler, restatements, obvious observations.

## Execution — 3 Passes

### Pass 1: Extract

List every distinct finding, fact, or decision from the source material as raw bullet points.
Do not compress yet — capture everything. Annotate confidence if available: [HIGH] / [MED] / [LOW].

### Pass 2: Eliminate

Remove any bullet that is:
- A restatement of another bullet
- An obvious inference any reader would make
- A hedging qualifier without substance ("it may be possible that...")
- Background context that does not inform a decision

### Pass 3: Compress

Merge related bullets into single dense sentences.
Format: fact + source-anchor + implication (if non-obvious).
Target: ≤40% of original bullet count, 0% information loss.

## Output Structure

```
## Synthesis: {Topic}

**Confidence Distribution:** {N} HIGH / {N} MED / {N} LOW findings

### Key Findings
[HIGH] {Finding} — {Source anchor}
[MED]  {Finding} — {Source anchor}
[LOW]  {Finding, flagged as unverified} — {Source anchor}

### Synthesis Paragraph
{Single paragraph: all HIGH and MED findings compressed into maximum density.
No LOW findings. No hedging. No filler. Every sentence decides something.}

### Remaining Uncertainties
{Only present if LOW findings exist or gaps were not resolved.
One bullet per unresolved gap — what is still unknown and why it matters.}
```

## Quality Gate

Before finalising: read the Synthesis Paragraph aloud (mentally).
If any sentence could be removed without losing information → remove it.
If any sentence requires background knowledge to understand → add one clause of context, then compress again.
