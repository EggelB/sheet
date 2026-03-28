# Decision Tree: Memory Checkpoints

**Purpose:** Evaluate whether to create memory checkpoint or continue working.

**When to Load:** When evaluating checkpoint triggers (per TIER 1, Rule 10: Proactive Checkpoints).

---

## CHECKPOINT TRIGGER EVALUATION

**Master Decision Tree:**

```
START: Checkpoint trigger detected
    ↓
EVALUATE: Which trigger fired?
    ├─ 15+ tool calls in single phase
    ├─ 5+ files modified
    ├─ Before Layer 3 start
    ├─ After Layer 4 audit
    └─ 3+ phases without memory commit
        ↓
ROUTE to trigger-specific evaluation
    ↓
DECISION: Checkpoint now OR Continue?
    ↓
IF CHECKPOINT → ASK user (never auto-write)
IF CONTINUE → Proceed with work
```

---

## TRIGGER 1: 15+ TOOL CALLS IN SINGLE PHASE

**Context:** Working on single phase, tool call count reaches 15+.

### Evaluation Flowchart

```
START: Tool call count ≥ 15
    ↓
Q1: Has significant new context been discovered?
    ├─ YES → Continue to Q2
    └─ NO → CONTINUE (routine operations, nothing to preserve)
         ↓
Q2: Are there technical decisions made?
    ├─ YES → Continue to Q3
    └─ NO → CONTINUE (mechanical work, no decision debt)
         ↓
Q3: Is phase >80% complete?
    ├─ YES → CONTINUE (almost done, checkpoint after completion)
    └─ NO → CHECKPOINT (complex phase, preserve mid-phase state)
```

### Significant Context Examples

**Checkpoint Worthy:**
- Discovered existing API constraints not in original spec
- Found edge cases requiring special handling
- Identified performance bottlenecks during exploration
- Uncovered technical debt that influenced implementation

**Not Checkpoint Worthy:**
- Reading files to understand code structure (routine)
- Running tests repeatedly (mechanical)
- Formatting code (trivial)
- Searching for variable names (routine)

### Decision Logic

**CHECKPOINT if:**
- ✅ Major discoveries (constraints, edge cases, patterns)
- ✅ Complex phase <80% complete
- ✅ Multiple architectural decisions made
- ✅ Risk of losing nuanced context in summarization

**CONTINUE if:**
- ✅ Routine file operations (reads, searches)
- ✅ Mechanical work (formatting, renaming)
- ✅ Phase almost complete (wait for completion checkpoint)
- ✅ No new learnings or decisions

---

## TRIGGER 2: 5+ FILES MODIFIED

**Context:** Modified 5 or more files in current session.

### Evaluation Flowchart

```
START: Modified file count ≥ 5
    ↓
Q1: Are changes part of single cohesive feature?
    ├─ YES → Continue to Q2
    └─ NO → CHECKPOINT (multiple independent changes, preserve context)
         ↓
Q2: Is feature complete and tested?
    ├─ YES → CHECKPOINT (logical completion point)
    └─ NO → Continue to Q3
         ↓
Q3: Are changes in multiple phases/modules?
    ├─ YES → CHECKPOINT (cross-cutting changes, high context)
    └─ NO → CONTINUE (single module, cohesive work)
```

### Decision Logic

**CHECKPOINT if:**
- ✅ Changes span multiple features/phases
- ✅ Feature complete (natural boundary)
- ✅ Cross-cutting changes (multiple modules affected)
- ✅ Complex refactoring with cascading effects

**CONTINUE if:**
- ✅ Single feature in progress (cohesive work)
- ✅ All changes in one module/phase
- ✅ Simple mechanical changes (renaming, moving files)
- ✅ Feature almost complete (wait for completion)

---

## TRIGGER 3: BEFORE LAYER 3 START

**Context:** About to start Layer 3 (Technical Blueprints) for a phase.

### Evaluation Flowchart

```
START: Layer 3 about to begin
    ↓
Q1: Is this the FIRST phase of Layer 3?
    ├─ YES → CHECKPOINT (preserve Layer 1+2 planning)
    └─ NO → Continue to Q2
         ↓
Q2: Is this a complex/high-risk phase?
    ├─ YES → CHECKPOINT (preserve pre-implementation state)
    └─ NO → Continue to Q3
         ↓
Q3: Has significant exploration occurred in Layers 1-2?
    ├─ YES → CHECKPOINT (preserve discovery context)
    └─ NO → CONTINUE (straightforward phase, minimal pre-work)
```

### Complex/High-Risk Phase Indicators

**High Risk:**
- Multiple external integrations
- Performance-critical code
- Security-sensitive logic
- Novel patterns (no existing examples in codebase)
- Large scope (>500 lines estimated)

**Low Risk:**
- CRUD operations (standard patterns)
- Single responsibility, isolated module
- Well-established patterns
- Small scope (<200 lines)

### Decision Logic

**CHECKPOINT if:**
- ✅ First phase (preserve all planning)
- ✅ High-risk/complex phase
- ✅ Extensive discovery in Layers 1-2
- ✅ Novel problem domain

**CONTINUE if:**
- ✅ Subsequent phase (planning already checkpointed)
- ✅ Low-risk, standard implementation
- ✅ Minimal pre-work (clear requirements from start)

---

## TRIGGER 4: AFTER LAYER 4 AUDIT

**Context:** Completed Layer 4 (DRY Audit) for a phase or entire project.

### Evaluation Flowchart

```
START: Layer 4 audit complete
    ↓
Q1: Were consolidations performed?
    ├─ YES → CHECKPOINT (preserve refactoring rationale)
    └─ NO → Continue to Q2
         ↓
Q2: Were temptations resisted (debt avoided)?
    ├─ YES → CHECKPOINT (preserve decision not to consolidate)
    └─ NO → CONTINUE (no significant findings)
```

### Decision Logic

**CHECKPOINT if:**
- ✅ Consolidations performed (document what & why)
- ✅ Consolidations rejected (document why not worth it)
- ✅ Significant code reduction achieved (>30%)
- ✅ Architectural patterns changed

**CONTINUE if:**
- ✅ No consolidation opportunities found
- ✅ Trivial audit (code already optimal)
- ✅ Proceeding immediately to Layer 5

---

## TRIGGER 5: 3+ PHASES WITHOUT MEMORY COMMIT

**Context:** Completed 3 phases without writing to memory.md.

### Evaluation Flowchart

```
START: 3+ phases completed since last checkpoint
    ↓
AUTOMATIC → CHECKPOINT
  (Too much context to risk losing in summarization)
```

### Decision Logic

**CHECKPOINT (automatic):**
- ✅ 3+ phases is guaranteed checkpoint
- ✅ Too much context accumulation
- ✅ Summarization would lose critical nuances

**Rationale:** Every 3 phases represents substantial work. Exceeding this threshold risks losing valuable context (decisions, failures, learnings) if conversation gets summarized.

---

## CHECKPOINT vs CONTINUE DECISION MATRIX

| Trigger | Checkpoint If | Continue If |
|---------|---------------|-------------|
| **15+ tool calls** | Major discoveries, <80% done | Routine ops, >80% done |
| **5+ files** | Multiple features, feature done | Single feature in progress |
| **Before Layer 3** | First phase or high-risk | Subsequent phase, low-risk |
| **After Layer 4** | Consolidations performed | No findings |
| **3+ phases** | ALWAYS | N/A (automatic) |

---

## CHECKPOINT EXECUTION PROTOCOL

**When decision is CHECKPOINT:**

### Step 1: ASK User (Never Auto-Write)

**Template:**

```
CHECKPOINT RECOMMENDED

Trigger: {Which trigger fired}
Context: {Brief summary of what was accomplished}
Reason: {Why checkpoint is valuable now}

Should I create memory checkpoint?
  - YES: I'll document {key points} in .github/memory.md
  - NO: Continue working (checkpoint deferred)
```

**Example:**

```
CHECKPOINT RECOMMENDED

Trigger: 15+ tool calls during Phase 2 implementation
Context: Discovered validation API constraints, implemented workaround
Reason: Complex phase with architectural decisions; preserve rationale

Should I create memory checkpoint?
  - YES: I'll document API constraints + workaround pattern
  - NO: Continue to Phase 3 (defer checkpoint)
```

---

### Step 2: If User Approves, Write Memory Entry

**Template (per `.github/memory.md` structure):**

```markdown
## [YYYY-MM-DD] {Project} - {Phase/Layer}
**What Was Built:** {Brief description}
**Technical Choices:** {Decisions made + rationale}
**Failures:** {What didn't work, why}
**Debt Avoided:** {Temptations resisted}
**Performance:** {Metrics if applicable}
**Learnings:** {Key insights}
```

**Keep entries dense (Chain-of-Density):**
- 50-100 words per entry
- Focus on decisions, not process
- Include gotchas and non-obvious learnings

---

### Step 3: Continue Work

After checkpoint written, proceed with next phase/layer.

---

## EDGE CASES

### Case 1: Multiple Triggers Simultaneously

**Scenario:** 15+ tool calls AND 5+ files modified.

**Decision:** Evaluate EACH trigger independently:
- If ANY trigger evaluates to CHECKPOINT → checkpoint
- If ALL triggers evaluate to CONTINUE → continue

**Most restrictive wins.**

---

### Case 2: User Says "NO" to Checkpoint

**Scenario:** Checkpoint recommended, user declines.

**Action:** 
- Respect user decision
- Continue working
- Next trigger re-evaluates (don't suppress)

**User can defer checkpoint but not permanently disable.**

---

### Case 3: Session Commands (User-Initiated)

**User says:** `checkpoint` or `save progress` or `session summary`

**Action:**
- IMMEDIATE checkpoint (bypass evaluation)
- User request overrides all heuristics
- Write memory entry
- Confirm completion

**User-initiated always honored.**

---

## ANTI-PATTERNS

### ❌ AVOID: Auto-Writing Memory Without Asking

**Wrong:**

```
[Tool calls reach 15]
Agent: [Writes to memory.md automatically]
```

**Problem:** Violates user control, disrupts flow.

**Right:**

```
[Tool calls reach 15]
Agent: "CHECKPOINT RECOMMENDED (15+ tool calls, complex phase).
        Should I create memory checkpoint?"
User: "Yes" or "No"
```

---

### ❌ AVOID: Ignoring 3+ Phases Trigger

**Wrong:**

```
[4 phases completed, no checkpoint]
Agent: [Continues to phase 5]
```

**Problem:** Too much context risk.

**Right:**

```
[3 phases completed]
Agent: "CHECKPOINT REQUIRED (3+ phases).
        Must document progress before continuing."
```

---

### ❌ AVOID: Checkpointing Trivial Progress

**Wrong:**

```
[5 files modified: renamed variables in each]
Agent: "Should I checkpoint?"
```

**Problem:** Wastes user time on mechanical changes.

**Right:**

```
[5 files modified: renamed variables]
Evaluation: Mechanical work, no decisions → CONTINUE
```

---

## MEMORY ARCHIVAL TRIGGER

**Separate from checkpoints:**

```
IF memory.md >500 lines:
    1. Create .github/archives/memory_archive_YYYYMMDD.md
    2. Move old entries (keep last 3 in active memory.md)
    3. Notify user of archival
```

**Archival is automatic, checkpoints require asking.**

---

## INTEGRATION WITH CCE WORKFLOW

**Throughout Workflow:**

Monitor triggers continuously:
- Track tool call count per phase
- Track file modification count
- Detect layer transitions
- Count phases since last checkpoint

**At Trigger Point:**

1. Load `.github/decision-trees/memory-checkpoints.md`
2. Evaluate trigger-specific flowchart
3. Decision: CHECKPOINT or CONTINUE
4. If CHECKPOINT → ASK user → Write if approved
5. If CONTINUE → Proceed with work

**Session Start:**

Read `.github/memory.md` for context from previous sessions.

---

## QUICK REFERENCE

**Checkpoint Evaluation Checklist:**

When trigger fires, ask:

- [ ] Significant new context discovered? (YES → lean toward checkpoint)
- [ ] Technical decisions made? (YES → lean toward checkpoint)
- [ ] Work almost complete? (YES → defer to completion checkpoint)
- [ ] Multiple independent changes? (YES → checkpoint)
- [ ] Complex/high-risk phase? (YES → checkpoint)
- [ ] 3+ phases since last checkpoint? (YES → MUST checkpoint)

**If ≥2 YES answers → CHECKPOINT**  
**If all NO → CONTINUE**

**Exception:** 3+ phases trigger is automatic (always checkpoint).

---

## VERIFICATION

**How to confirm checkpoint system works:**

### Test 1: Triggers Detected

- [ ] Agent detects when thresholds reached
- [ ] Agent evaluates decision tree (not auto-checkpoint)

### Test 2: User Control

- [ ] Agent ASKS before writing
- [ ] User can approve or decline
- [ ] Session commands honored immediately

### Test 3: Quality Entries

- [ ] Memory entries are dense (50-100 words)
- [ ] Focus on decisions, not process
- [ ] Include failures and avoided debt

**If auto-writing without asking → system broken, fix immediately.**
