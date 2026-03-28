# Prompt Library: Authoring Schema

Every file in `.github/prompts/` MUST begin with a YAML frontmatter block
conforming to this schema. No field is optional.

---
title: "Human-readable name (title case, ≤8 words)"
description: "One sentence: what this prompt does."
intent-tags: [tag1, tag2]
modes: [mode-name]  # or ["all"] for cross-mode prompts
output-format: "What the prompt produces (e.g. structured brief, mermaid diagram, ADR document)"
when-to-use: "1–2 sentences: the trigger condition that tells an agent when to reach for this prompt."
---

## Intent Tag Taxonomy (controlled vocabulary — do not add tags without extending this list)

| Tag | Meaning |
|---|---|
| `synthesis`       | Compressing multi-source content into a dense, signal-rich brief |
| `gap-analysis`    | Identifying what is still unknown after a reasoning or research pass |
| `research`        | Web-search-driven investigation and source cross-referencing |
| `decompose`       | Breaking an ambiguous goal into bounded, actionable sub-problems |
| `socratic`        | Driving clarification through targeted questioning sequences |
| `architecture`    | Designing system structure, component relationships, data flows |
| `decision-record` | Producing a structured Architecture Decision Record (ADR) |
| `diagram`         | Generating Mermaid or other visual representations of a system |
| `assess`          | Evaluating scope and complexity of a task before acting |
| `implement`       | Structured pattern for code-writing execution |
| `gate`            | Verification and quality-check before declaring work complete |
| `ambiguity`       | Resolving underspecified or conflicting requirements |

## Access Protocol

Agents MUST use `read_file` to load prompts by known filename.
For intent-based discovery: `grep_search` with `includeIgnoredFiles: true`,
searching `.github/prompts/` for `intent-tags:` containing the desired tag.
NEVER use `semantic_search` or `file_search` — neither finds `.github/` contents.
