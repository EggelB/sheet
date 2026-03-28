---
title: "Assess → Implement → Gate"
description: "Execute a development task through three disciplined stages: scope assessment with checklist, decisive implementation with opinionated defaults, and non-negotiable quality gate before declaring done."
intent-tags: [assess, implement, gate]
modes: ["quick-developer"]
output-format: "task execution log"
when-to-use: "For any development task that passes the complexity threshold: ≤5 files, ≤1 hour, no architectural decisions required, ≤1 new component. Load at the start of every Quick Developer session."
---

# Assess → Implement → Gate Protocol

## STAGE 1: ASSESS

### Actions (silent — no user interaction until checklist is ready)

1. Identify all files that will be read or modified
2. Identify all symbols that will be changed or added
3. Restate the task: "I will {verb} {what} in {where} so that {outcome}."
4. List every planned change as a numbered checklist item

### Checklist Format

```
## Task: {One-sentence restatement}

### Planned Changes
- [ ] {File or symbol}: {What changes and why}

### Opinionated Defaults
- Commented-out code: never — delete or don't add
- Functions >20 lines: comment explaining WHY, not just what
- No TODOs, stubs, unimplemented placeholders
- Python: type annotations + docstrings on all public functions
- C#: XML doc comments on public members; nullable annotations always
- TypeScript: JSDoc on exports; no implicit `any`

### Ready? (confirm or correct)
```

Present checklist. Wait for confirmation. One correction round maximum.

---

## STAGE 2: IMPLEMENT

### Entry condition: user confirmed checklist

- Follow the checklist exactly — no scope creep
- Decisions (X vs Y): pick the better option, note it, move on. Do NOT ask.
- Apply all opinionated defaults — no exceptions
- No TODOs, stubs, `pass` without implementation
- Hidden dependency found: add to checklist, state it, implement it

### Done when: all checklist items checked off, zero unresolved items.

---

## STAGE 3: GATE

### Entry condition: all checklist items complete

1. Run `tempo.executor run_quality_gates` — lint at minimum
2. PASS → Completion Statement
3. FAIL → fix all, re-run. Repeat until zero-exit. Never declare done on a failing gate.

### Completion Statement

```
## Gate Passed ✓
**Task:** {One-sentence restatement}
**Files changed:** {list}
**Gate:** lint passed (0 violations)
**Choices made:** {what was chosen and why — one line per non-obvious choice}
**Memory updated:** yes
```

### Memory write (mandatory on gate pass)

`tempo.memory write_memory`: `what_was_built`, `technical_choices`, `learnings`
