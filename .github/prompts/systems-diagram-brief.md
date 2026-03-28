---
title: "Systems Diagram Brief"
description: "Produce a paired Mermaid architecture diagram and Component Inventory table, with an explicit Boundary Decisions section that forces the system scope to be owned as a design choice."
intent-tags: [diagram, architecture]
modes: ["strategic-collaborator"]
output-format: "Mermaid diagram + component inventory"
when-to-use: "Whenever you need to visualise a system's structure, establish its boundary, or communicate component relationships. Always produce diagram + inventory + boundary decisions together — never separately."
---

# Systems Diagram Brief Protocol

## The Three-Part Rule

A system diagram is complete only when all three parts are present — always produced together:
1. **Component Inventory** — what every piece is and what it does
2. **Mermaid Diagram** — how the pieces relate and communicate
3. **Boundary Decisions** — what is explicitly IN scope vs OUT of scope

## Part 1: Component Inventory

```
### Component Inventory: {System Name}
| Component | Type | Responsibility | Key Interfaces | External? |
|---|---|---|---|---|
| {Name} | Service/Store/UI/Job/Gateway | One sentence: singular job | Exposed + consumed | Yes/No |
```

- Every component in the diagram must have a row
- "Responsibility" = one sentence. Two sentences = two responsibilities (split it)
- External? = Yes if outside your system boundary

## Part 2: Mermaid Diagram

```
graph TD
    subgraph "System Boundary: {System Name}"
        A[Component A]
        B[Component B]
    end
    EXT1([External: {Name}])
    EXT1 -->|protocol/data| A
    A -->|protocol/data| B
```

- System boundary ALWAYS drawn as `subgraph`
- External dependencies use round brackets `([...])`
- Edge labels name protocol/data type where non-obvious
- No more than 12 nodes — split into sub-diagrams if larger

## Part 3: Boundary Decisions

```
### Boundary Decisions: {System Name}
**In scope:** {component/concern}: {why inside boundary}
**Out of scope:** {component/concern}: {why outside + who owns it}
**Deferred:** {component/concern}: {what info is needed to decide}
```

AI drafts; human approves. Ambiguous boundary not decided here = ownership conflict during implementation.

## Versioning

Diagram updated: increment title to "v{N+1}", note what changed from v{N}, write prior version to `tempo.memory` before overwriting.
