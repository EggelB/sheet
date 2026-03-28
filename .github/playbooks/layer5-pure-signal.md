# Layer 5 Playbook: Pure Signal Implementation

**Purpose:** Distill Layers 1-4 into dense, executable technical brief to serve as the anchor for subsequent autonomous implementation.

---

## PRE-FLIGHT CHECKLIST

**Before starting Layer 5:**

- [ ] Layer 4 consolidations executed and approved
- [ ] All approved DRY improvements applied to Layer 3
- [ ] **CRITICAL:** Load `.github/exploits/chain-of-density.md` for merge methodology
- [ ] Layer 1 file accessible (for WHY context)
- [ ] Post-consolidation Layer 3 complete (for HOW details)

---

## CHAIN-OF-DENSITY MERGE PROTOCOL

### Purpose: Merge WHY + HOW into Dense Technical Brief

**Goal:** Create document that contains:

- **Strategic context** (from Layer 1: why each phase exists)
- **Technical implementation** (from post-consolidation Layer 3: exact code)
- **Zero narrative fluff** (no "we will", "let's", "here's how")
- **Maximum information density** per line

### Merge Methodology

#### Step 1: Extract WHY from Layer 1

For each phase, capture:

- **Justification:** Why this phase exists
- **What it enables:** How it supports overall goal
- **Success criteria:** What "done" means

**Example extraction:**

```
Phase 2 WHY: "Data processing pipeline provides clean, validated customer data 
for Phase 3 analytics. Success = schema-compliant records persisted to target."
```

#### Step 2: Extract HOW from Layer 3 (Post-Consolidation)

For each phase, capture:

- **Key functions/classes:** What gets built
- **Core algorithms:** Critical logic patterns
- **Integration points:** Dependencies, data flows
- **Edge cases handled:** Error scenarios covered

**Example extraction:**

```
Phase 2 HOW: 
- CustomerRepository.validate_and_transform(raw_data) -> Customer
- Single-pass O(n) validation + transformation + persistence
- Handles: missing fields (raise ValueError), type mismatches (coerce), duplicates (skip)
- Integration: Reads from source DB, writes to analytics DB
```

#### Step 3: Merge into Dense Entries

**Format:**

```markdown
### Phase N: {Name}

**Context:** {WHY from Layer 1 - 1-2 sentences}

**Implementation:**
- **Primary Components:** {Key classes/functions}
- **Algorithm:** {Core logic pattern}
- **Data Flow:** {Input → Process → Output}
- **Edge Cases:** {Error handling}
- **Dependencies:** {What must exist first}
- **Verification:** {How to test completion}

**Code Anchor:**
```python
{Paste critical function signatures and core logic - NOT full implementation}
```

```

#### Step 4: Noise Elimination

**DELETE from Layer 5:**
- Explanations of standard concepts
- Motivational/conversational language
- Redundant descriptions
- Tutorial-style walkthroughs
- Uncertainty phrases ("should", "might", "could")

**KEEP in Layer 5:**
- Strategic rationale
- Technical specifications
- Critical algorithms
- Integration contracts
- Verification criteria

---

## LAYER 5 OUTPUT TEMPLATE

```markdown
# {Project Name} - Layer 5: Pure Signal Implementation

**Goal:** {From Layer 1 - single sentence}

**Phases:** {List phase names for quick reference}

---

## Phase 1: {Name}

**Context:** {WHY: Business justification from Layer 1}

**Implementation:**
- **Primary:** {Key class/function names}
- **Algorithm:** {Core pattern, e.g., "Single-pass validation with hash-based deduplication"}
- **Flow:** {Input type} → {Process} → {Output type}
- **Errors:** {Handled scenarios}
- **Dependencies:** {Prerequisites}
- **Verification:** {Test command or acceptance check}

**Anchor:**
```python
class CustomerRepository:
    def validate_and_transform(self, raw: Dict[str, Any]) -> Customer:
        # Single-pass validation + transformation
        if not all(k in raw for k in ['id', 'name', 'email']):
            raise ValueError("Missing required fields")
      
        return Customer(
            id=str(raw['id']),
            name=raw['name'].strip(),
            email=raw['email'].lower()
        )
```

---

## Phase 2:

{Repeat structure}

---

## Verification Matrix

| Phase | Verification Command            | Success Criteria                       |
| ----- | ------------------------------- | -------------------------------------- |
| 1     | `pytest tests/test_phase1.py` | All tests pass, >80% coverage          |
| 2     | `pytest tests/test_phase2.py` | All tests pass, integration successful |
| N     | `pytest tests/`               | Full suite passes, zero-exit           |

---

## Execution Checklist

- [ ] Phase 1 implemented
- [ ] Phase 1 tests pass
- [ ] Phase 2 implemented
- [ ] Phase 2 tests pass
- [ ] Phase N implemented
- [ ] Phase N tests pass
- [ ] Linting passes (zero errors/warnings)
- [ ] Security scan passes (zero high/critical)
- [ ] Full integration test passes

**Status:** Layer 5 complete when all checkboxes marked

```

---

## IMPLEMENTATION EXECUTION PROTOCOL

### Step 1: Create Layer 5 Document

Generate `{project}_layer5_pure_signal.md` using Chain-of-Density merge.

### Step 2: Sequential Phase Implementation

**For EACH phase:**

1. **Read Phase Context** from Layer 5
2. **Implement Code** based on technical anchor
3. **Write Tests** per verification criteria
4. **Run Tests** → Must pass before proceeding
5. **Update Checklist** → Mark phase complete
6. **Commit Progress** (optional but recommended)

**DO NOT skip to next phase if current tests failing**

### Step 3: Linting Gate

After all phases implemented:

```bash
# Python
pylint src/
flake8 src/
mypy src/

# TypeScript
eslint src/
tsc --noEmit

# General
# All linters must return zero-exit
```

**If linting fails → fix issues before proceeding**

### Step 4: Security Scan Gate

```bash
# Python
bandit -r src/
safety check

# Node.js
npm audit
snyk test

# All scans must show zero high/critical vulnerabilities
```

**If security issues found → remediate before proceeding**

### Step 5: Integration Testing

Run full test suite:

```bash
pytest tests/ --cov --cov-report=html
# OR
npm test -- --coverage

# Requirements:
# - All tests pass (zero failures)
# - Coverage >80% for critical paths
# - Zero-exit code
```

**If integration fails → debug and fix before marking complete**

---

## ZERO-EXIT VERIFICATION GATES

**Layer 5 is NOT "done" until:**

✅ **Unit Tests:** Zero failures
✅ **Integration Tests:** Zero failures
✅ **Linting:** Zero errors, zero warnings
✅ **Security Scan:** Zero high/critical vulnerabilities
✅ **Coverage:** >80% for critical business logic
✅ **Manual Smoke Test:** Core user flow works end-to-end

**Any gate fails → revert to Layer 3 of failing phase → re-evaluate logic → re-implement**

---

## DENSITY VALIDATION CRITERIA

**Layer 5 document must be:**

### High Signal-to-Noise

**Calculate:**

```
Signal = Technical specs + rationale + code anchors
Noise = Explanations + motivation + uncertainty

Target: Signal/Noise ratio > 5:1
```

**Example HIGH density:**

```markdown
### Phase 2: ETL Pipeline

**Context:** Provides schema-validated customer data for analytics (Phase 3 dependency).

**Implementation:**
- **Primary:** ETLPipeline.process_batch(records: List[Dict]) -> List[Customer]
- **Algorithm:** Single-pass O(n) validate→transform→persist with error isolation
- **Flow:** Raw DB records → Validation → Customer objects → Analytics DB
- **Errors:** Missing fields (ValueError), type errors (coerce or skip), duplicates (last-write-wins)
- **Verification:** `pytest tests/test_etl.py` - All pass, 10k records in <2s
```

**Example LOW density (AVOID):**

```markdown
### Phase 2: ETL Pipeline

In this phase, we're going to build an ETL (Extract, Transform, Load) pipeline. 
This is important because we need to get data from one place to another. We'll 
start by extracting the data, then we'll transform it to make sure it's clean, 
and finally we'll load it into the target system. This will help us prepare for 
the next phase where we'll do analytics.
```

---

## LANGUAGE-SPECIFIC EXECUTION PATTERNS

### Python

**Structure:**

```
src/
  {project}/
    __init__.py
    models.py          # Data classes
    repositories.py    # Data access
    services.py        # Business logic
    utils.py           # Utilities
tests/
  test_models.py
  test_repositories.py
  test_services.py
  conftest.py          # Fixtures
```

**Test Execution:**

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest tests/ --cov=src --cov-report=term --cov-report=html

# Lint
pylint src/
mypy src/

# Security
bandit -r src/
```

### TypeScript/JavaScript

**Structure:**

```
src/
  models/
  repositories/
  services/
  utils/
tests/
  models.test.ts
  repositories.test.ts
package.json
tsconfig.json
```

**Test Execution:**

```bash
# Install
npm install

# Run tests
npm test

# Lint
npm run lint

# Type check
npm run type-check

# Security
npm audit
```

---

## FAILURE RECOVERY PROTOCOL

### If Tests Fail

1. **Identify failing phase** from test output
2. **Read Layer 5 anchor** for that phase
3. **Compare implementation** to anchor specification
4. **Check Layer 3 blueprint** for that phase (post-consolidation)
5. **Identify logic error** (incorrect algorithm, missing validation, etc.)
6. **Fix implementation**
7. **Re-run tests**
8. **Repeat until zero-exit**

### If Linting Fails

1. **Read linter output** for specific violations
2. **Fix code style issues** (formatting, naming, imports)
3. **Re-run linter**
4. **Repeat until zero warnings/errors**

### If Security Scan Fails

1. **Review vulnerability report** for affected dependencies/code
2. **Update vulnerable dependencies** to patched versions
3. **Refactor vulnerable code patterns** (SQL injection, XSS, etc.)
4. **Re-run scan**
5. **Repeat until zero high/critical**

### If Integration Test Fails

1. **Identify breaking point** in end-to-end flow
2. **Check phase dependencies** in Layer 5 verification matrix
3. **Verify prerequisite phases** are fully functional
4. **Debug integration contract** (data format, API contract, etc.)
5. **Fix integration issue**
6. **Re-run integration tests**
7. **Repeat until full suite passes**

---

## IMPLEMENTATION ANTI-PATTERNS

### ❌ AVOID: Implementing before Layer 5 complete

**Bad:** Start coding during Layer 3
**Good:** Complete Chain-of-Density merge first, then implement

### ❌ AVOID: Skipping verification gates

**Bad:** "Tests mostly pass, shipping it"
**Good:** Fix all failures, achieve zero-exit on all gates

### ❌ AVOID: Implementing out of phase order

**Bad:** Jump to Phase 3 because it's more interesting
**Good:** Sequential implementation (1→2→3) to satisfy dependencies

### ❌ AVOID: Adding features not in Layer 5

**Bad:** "While I'm here, let me add this cool feature"
**Good:** Implement ONLY what's in Layer 5. New features = new Layer 1

### ❌ AVOID: Verbose Layer 5 documents

**Bad:** Layer 5 is longer than Layer 3
**Good:** Layer 5 is 40-60% the size of Layer 3 (pure signal extraction)

---

## SUCCESS METRICS

**Layer 5 completion indicates:**

1. **Code Exists:** All phases implemented in runnable form
2. **Tests Pass:** Zero failures across all test suites
3. **Quality Gates:** Linting, security, coverage all green
4. **Documentation:** Layer 5 serves as maintenance anchor
5. **Repeatability:** New developer can implement from Layer 5 alone
6. **Traceability:** Every function traces to Layer 5 phase
7. **Completeness:** All Layer 1 goals achieved

---

## POST-IMPLEMENTATION ACTIONS

### Update Memory

Write to `.github/memory.md`:

```markdown
## [2026-02-04] {Project Name} - Layer 5 Complete

**What Was Built:** {Brief summary of all phases}

**Technical Choices:**
- {Key architectural decisions}
- {Libraries/frameworks used}
- {Performance optimizations applied}

**Failures Encountered:**
- {What didn't work initially}
- {How issues were resolved}

**Debt Avoided:**
- {Premature optimizations resisted}
- {Consolidations that prevented bloat}

**Performance Metrics:**
- Test runtime: {duration}
- Coverage: {percentage}
- Build time: {duration}

**Key Learnings:**
- {Insights for future similar projects}
- {What would be done differently}
```

### Archive Layer Documents

**Keep active:**

- `{project}_layer5_pure_signal.md` - Primary reference for maintenance

**Archive (optional):**

- `{project}_layer1_strategic.md` - Historical context
- Layers 2-4 merged into Layer 1 file - Can be deleted after Layer 5 complete

---

## HANDOFF PROTOCOL

**Layer 5 document enables:**

1. **New team member onboarding:** Read Layer 5 → understand entire system
2. **Bug investigation:** Trace function → find in Layer 5 → understand intent
3. **Feature additions:** New feature = new Layers 1-5 cycle
4. **Refactoring:** Layer 5 describes WHAT must be preserved during HOW changes
5. **Documentation:** Layer 5 IS the technical documentation

**Layer 5 as Living Document:**

- Update when implementation deviates from plan (keep in sync)
- Annotate with production learnings
- Serves as regression testing guide

---

## SIGN-OFF PROTOCOL

**After implementing all phases and passing all gates:**

1. **Present completion summary:**
   - All phases implemented: ✅
   - Tests passing: ✅ (show zero-exit confirmation)
   - Linting clean: ✅
   - Security scan clear: ✅
   - Coverage achieved: {percentage}
2. **Demonstrate core user flow** (manual smoke test)
3. **Show Layer 5 document** as maintenance anchor
4. **Request final sign-off:** "Project implementation complete. Ready for deployment/next phase?"

**Project is "done" when user confirms acceptance**

---

## QUALITY GATES SUMMARY

**Before marking Layer 5 complete:**

- [ ] Layer 5 document created with Chain-of-Density merge
- [ ] All phases implemented sequentially
- [ ] Unit tests: Zero failures
- [ ] Integration tests: Zero failures
- [ ] Linting: Zero errors/warnings
- [ ] Security scan: Zero high/critical vulnerabilities
- [ ] Coverage: >80% for critical paths
- [ ] Manual smoke test: Core flow functional
- [ ] Memory updated with learnings
- [ ] User sign-off received

**ALL checkboxes must be marked before considering project complete**
