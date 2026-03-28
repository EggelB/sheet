# Decision Tree: Ambiguity Resolution

**Purpose:** Systematic framework for classifying and resolving ambiguous scenarios during development.

**When to Load:** When ambiguous scenario encountered (per TIER 1, Rule 1: "If ambiguous → STOP and ask").

---

## AMBIGUITY CLASSIFICATION FRAMEWORK

**First Step:** Identify which type of ambiguity blocks progress.

```
START: Ambiguity detected
    ↓
CLASSIFY into one of 6 types:
├─ 1. SCOPE Ambiguity
├─ 2. SPECIFICATION Ambiguity
├─ 3. CONSTRAINT Ambiguity
├─ 4. TRADE-OFF Ambiguity
├─ 5. ARCHITECTURAL Ambiguity
└─ 6. PRIORITY Ambiguity
    ↓
ROUTE to corresponding resolution protocol
```

---

## TYPE 1: SCOPE AMBIGUITY

**Definition:** Unclear boundaries - what's included/excluded from implementation.

### Indicators

- User says "add validation" without specifying which functions
- "Improve error handling" without defining scope
- "Refactor module" without boundaries
- Unclear if change applies to one component or system-wide

### Resolution Protocol

```
STEP 1: Identify scope dimensions
    - Which files/modules?
    - Which functions/classes?
    - Which data/inputs?

STEP 2: Present bounded options
    Option A: Minimal scope (specific component)
    Option B: Moderate scope (related components)
    Option C: Maximal scope (entire subsystem)

STEP 3: Ask clarifying question
    "Should {change} apply to:
     A) Only {specific}
     B) All {category}
     C) {Alternative interpretation}"
```

### Example

**Ambiguous:** "Add logging"

**Resolution:**

```
SCOPE DIMENSIONS:
- Which modules: Current module or all?
- Which level: Debug, Info, Warning, Error?
- Which events: Function entry/exit or specific events?

QUESTION:
Should logging apply to:
A) Only new validation function (minimal)
B) All validation functions in module (moderate)
C) All functions across codebase (maximal)

And log:
A) Function entry/exit (detailed)
B) Only errors (essential)
```

**User answers → Scope clarified → Proceed**

---

## TYPE 2: SPECIFICATION AMBIGUITY

**Definition:** Unclear behavior definition - what constitutes success/failure.

### Indicators

- "Validate data" without specifying rules
- "Process records" without defining processing steps
- "Handle errors" without specifying how
- Missing acceptance criteria

### Resolution Protocol

```
STEP 1: Identify specification gaps
    - Input format/constraints
    - Output format/guarantees
    - Success criteria
    - Failure behavior
    - Edge cases

STEP 2: Request concrete examples
    "Can you provide:
     - Example valid input → expected output
     - Example invalid input → expected behavior
     - Edge case: {scenario} → {expected}?"

STEP 3: Propose specification template
    INPUT: {type, constraints}
    OUTPUT: {type, guarantees}
    SUCCESS: {criteria}
    FAILURE: {behavior - throw, return, log?}
    EDGES: {null, empty, invalid, boundary cases}
```

### Example

**Ambiguous:** "Validate email addresses"

**Resolution:**

```
SPECIFICATION GAPS:
- What rules? (Format only? DNS check? Deliverability?)
- On failure: Throw exception or return result?
- Edge cases: Empty string? Null? Multiple @? International domains?

REQUEST EXAMPLES:
- Valid: "user@example.com" → {what}?
- Invalid: "notanemail" → {throw or return false}?
- Edge: "user+tag@subdomain.example.co.uk" → {valid or invalid}?

PROPOSED SPEC:
INPUT: String (email address)
OUTPUT: Boolean OR ValidationResult
SUCCESS: Contains @ and valid domain format
FAILURE: Return false OR throw ValidationError
EDGES:
  - Empty/null: Invalid
  - Plus addressing (user+tag@): Valid or invalid?
  - International domains: Valid or invalid?
```

**User answers → Specification complete → Implement**

---

## TYPE 3: CONSTRAINT AMBIGUITY

**Definition:** Unclear hard requirements or limitations.

### Indicators

- "Use existing API" without specifying which parts
- "Must be fast" without performance target
- "Keep it simple" without complexity budget
- "Integrate with {system}" without interface details

### Resolution Protocol

```
STEP 1: Identify constraint categories
    - Technical: Performance, compatibility, dependencies
    - Functional: Must-have vs nice-to-have
    - Operational: Deployment, monitoring, maintenance
    - Business: Budget, timeline, compliance

STEP 2: Quantify vague constraints
    "Fast" → "How fast? <50ms? <500ms?"
    "Simple" → "How simple? <100 lines? No external deps?"
    "Integrate" → "Which API endpoints? Auth method?"

STEP 3: Ask for hard limits
    "What are hard constraints (must-have)?
     What are soft preferences (nice-to-have)?"
```

### Example

**Ambiguous:** "Make validation faster"

**Resolution:**

```
CONSTRAINT CATEGORIES:
- Performance: Current speed? Target speed? Latency budget?
- Resources: Can use caching? Memory budget? CPU budget?
- Compatibility: Must work with existing code? API stable?
- Trade-offs: Willing to sacrifice accuracy for speed?

QUANTIFY:
- Current: {measure if available} or unknown?
- Target: <50ms? <100ms? <500ms?
- Acceptable trade-offs:
  A) 10x faster, 50MB memory → OK?
  B) 3x faster, no memory increase → better?
  C) 5x faster, added complexity → acceptable?

HARD CONSTRAINTS:
- Must: {absolute requirements}
- Should: {preferences}
- Nice-to-have: {optional improvements}
```

**User specifies → Constraints clear → Design within bounds**

---

## TYPE 4: TRADE-OFF AMBIGUITY

**Definition:** Multiple valid approaches with different costs/benefits, unclear which user prefers.

### Indicators

- Multiple design patterns fit
- Optimization has trade-offs (speed vs memory vs complexity)
- Competing goals (flexibility vs simplicity)
- No dominant solution

### Resolution Protocol

```
STEP 1: Enumerate options
    For each option:
    - Approach description
    - Benefits
    - Costs/drawbacks
    - Best fit scenario

STEP 2: Present decision matrix
    | Option | Speed | Memory | Complexity | Best For |
    |--------|-------|--------|------------|----------|
    | A      | +++   | -      | ++         | {scenario} |
    | B      | +     | +++    | +          | {scenario} |
    | C      | ++    | ++     | ---        | {scenario} |

STEP 3: Ask priority question
    "Which factor is most important:
     A) Performance (optimize speed)
     B) Resource efficiency (minimize memory)
     C) Maintainability (keep simple)
     D) Flexibility (future extensions)"
```

### Example

**Ambiguous:** "Improve validation performance"

**Resolution:**

```
OPTIONS:

OPTION A: In-memory caching
  ✅ Benefits: 10x faster lookups
  ❌ Costs: 50MB memory, stale data risk
  Best for: Read-heavy workloads, stable validation rules

OPTION B: Optimized regex patterns
  ✅ Benefits: 3x faster, no memory increase
  ❌ Costs: Increased code complexity
  Best for: CPU-bound validation, memory-constrained

OPTION C: Parallel processing
  ✅ Benefits: 5x faster with multiple cores
  ❌ Costs: Threading complexity, harder to debug
  Best for: Batch validation, multi-core environments

DECISION MATRIX:
| Option | Speed | Memory | Complexity | Stability |
|--------|-------|--------|------------|-----------|
| Cache  | +++   | --     | +          | Needs invalidation |
| Regex  | ++    | +++    | --         | Stable |
| Parallel| +++  | +      | ---        | Complex debugging |

QUESTION:
What's your priority?
A) Maximum speed (choose Cache or Parallel)
B) Minimal resource use (choose Regex)
C) Simplest implementation (choose Regex)
D) Balanced (Regex or Cache with short TTL)
```

**User prioritizes → Option selected → Implement**

---

## TYPE 5: ARCHITECTURAL AMBIGUITY

**Definition:** Unclear which design pattern or code structure to use.

### Indicators

- "Refactor for flexibility" without specifying flexibility type
- Multiple patterns fit (Strategy vs Template vs Decorator)
- Unclear if need class vs function
- Uncertain abstraction level

### Resolution Protocol

```
STEP 1: Identify architectural decision point
    - Pattern selection (Factory vs Builder)
    - Abstraction level (Function vs Class)
    - Error handling (Exception vs Return)
    - Concurrency model (Sync vs Async)

STEP 2: Load architecture decision tree
    → `.github/decision-trees/architecture-choices.md`
    Apply relevant flowchart

STEP 3: If decision tree unclear
    → Load `.github/exploits/socratic-questioning.md`
    Ask about:
    - Primary use case
    - Expected evolution
    - Integration points
    - Complexity budget
```

### Example

**Ambiguous:** "Make validation more flexible"

**Resolution:**

```
ARCHITECTURAL DECISION: What kind of flexibility?

OPTION A: Runtime validator switching
  Pattern: Strategy Pattern
  Use case: Different validation rules per user/tenant
  Complexity: Moderate

OPTION B: Composable validation rules
  Pattern: Decorator/Builder Pattern
  Use case: Stack multiple validators, configure combinations
  Complexity: High

OPTION C: Configurable validation
  Pattern: Config-driven (YAML/JSON)
  Use case: Non-developers modify rules
  Complexity: Low

LOAD: .github/decision-trees/architecture-choices.md
      → Strategy vs Builder decision flowchart

QUESTION:
Flexibility for whom and when?
A) Developers at compile-time (Strategy)
B) Developers building complex combinations (Builder)
C) Users/admins at runtime (Config-driven)

How often do rules change?
A) Rarely (hardcode)
B) Frequently (config-driven)
C) Per-request (runtime switching)
```

**User clarifies → Pattern selected → Implement**

---

## TYPE 6: PRIORITY AMBIGUITY

**Definition:** Multiple tasks requested, unclear execution order or resource allocation.

### Indicators

- "Fix bugs and add features" without priority
- "Refactor and optimize" without sequence
- Limited time/budget, unclear what's essential
- Conflicting deadlines

### Resolution Protocol

```
STEP 1: Enumerate tasks
    List all requested work items

STEP 2: Identify dependencies
    Which tasks block others?
    Which are independent?

STEP 3: Present sequencing options
    Option A: Sequential (Task 1 → Task 2 → ...)
    Option B: Parallel (separate work streams)
    Option C: Phased (MVP → enhancements)

STEP 4: Ask priority question
    "Given {constraints}, what's the priority?
     A) {Task 1} first (rationale)
     B) {Task 2} first (rationale)
     C) Both parallel (requires resources)
     D) {Task 1} only, defer {Task 2}"
```

### Example

**Ambiguous:** "Fix validation bugs and add new email validator"

**Resolution:**

```
TASKS:
1. Fix existing validation bugs
2. Add email validator feature

DEPENDENCIES:
- Tasks are independent (can be parallel)
- Bug fixes may affect email validator design

SEQUENCING OPTIONS:

OPTION A: Bugs first, then feature
  ✅ Stable foundation before new code
  ❌ Feature delayed

OPTION B: Feature first, then bugs
  ✅ Deliver feature faster
  ❌ Build on potentially buggy base

OPTION C: Parallel
  ✅ Both delivered simultaneously
  ❌ Potential conflicts, needs coordination

OPTION D: Bugs only
  ✅ Focus on stability
  ❌ Feature indefinitely deferred

QUESTION:
What's driving priority?
A) Production issues (bugs critical) → Option A
B) Customer commitment (feature deadline) → Option B
C) Sufficient resources (2+ devs) → Option C
D) Stability focus (feature nice-to-have) → Option D
```

**User specifies → Priority clear → Sequence work**

---

## RESOLUTION DECISION TREE

**Master Flowchart:**

```
START: Ambiguity detected
    ↓
Q1: What's ambiguous?
    ├─ "What to build/change?" → SCOPE ambiguity
    ├─ "How should it behave?" → SPECIFICATION ambiguity
    ├─ "What are the limits?" → CONSTRAINT ambiguity
    ├─ "Which approach?" → TRADE-OFF ambiguity
    ├─ "Which pattern?" → ARCHITECTURAL ambiguity
    └─ "What order?" → PRIORITY ambiguity
         ↓
ROUTE to type-specific protocol
    ↓
EXECUTE resolution steps
    ↓
Q2: Ambiguity resolved?
    ├─ YES → Document decision → Proceed
    └─ NO → Load `.github/exploits/socratic-questioning.md`
              → Deep exploration → Return to classification
```

---

## ANTI-PATTERNS

### ❌ AVOID: Guessing Instead of Asking

**Wrong:**

```
User: "Add validation"
Agent: [Implements email validation because it seems common]
```

**Right:**

```
User: "Add validation"
Agent: "SCOPE AMBIGUITY: What should be validated?
        A) Email format only
        B) All user input fields
        C) Business rules (age >18, etc.)"
```

---

### ❌ AVOID: Asking Open-Ended Questions

**Wrong:**

```
"How should validation work?"
```

**Right:**

```
"SPECIFICATION: On validation failure, should we:
 A) Throw ValidationError exception
 B) Return ValidationResult{valid: false, errors: [...]}
 C) Log error and continue"
```

---

### ❌ AVOID: Proceeding with Partial Clarity

**Wrong:**

```
User clarified scope but not behavior → Agent implements anyway
```

**Right:**

```
User clarified scope but not behavior → Agent asks:
"Scope clear (all validation functions). Still unclear:
 On validation failure, should we throw or return result?"
```

---

## INTEGRATION WITH CCE WORKFLOW

**Layer 1 (Strategic Summary):**
- If user goal is ambiguous → STOP
- Load this decision tree
- Classify ambiguity type
- Execute resolution protocol
- Generate Layer 1 only after clarity

**Layer 2 (Operational Granularity):**
- If task interpretation ambiguous → STOP
- Classify and resolve
- Proceed with zero-ambiguity tasks

**Layer 3 (Technical Blueprints):**
- If implementation approach ambiguous → STOP
- Classify (likely ARCHITECTURAL or TRADE-OFF)
- Cross-reference `.github/decision-trees/architecture-choices.md`
- If still unclear → `.github/exploits/socratic-questioning.md`

**Rule:** Never guess. Always classify → resolve → proceed.

---

## QUICK REFERENCE

| Ambiguity Type | Key Question | Resolution Tool |
|----------------|--------------|-----------------|
| **SCOPE** | What's included/excluded? | Bounded options (minimal/moderate/maximal) |
| **SPECIFICATION** | How should it behave? | Concrete examples + spec template |
| **CONSTRAINT** | What are the limits? | Quantify vague terms + hard vs soft |
| **TRADE-OFF** | Which approach? | Decision matrix + priority question |
| **ARCHITECTURAL** | Which pattern? | Architecture decision tree + use case analysis |
| **PRIORITY** | What order? | Dependency analysis + sequencing options |

**Default Action:** When in doubt → `.github/exploits/socratic-questioning.md`
