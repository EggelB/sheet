# Layer 1 Playbook: Strategic Summary

**Purpose:** Transform user goal into high-level development phases with clear plan summaries and justifications.

---

## PRE-FLIGHT CHECKLIST

**Before generating Layer 1:**

- [ ] User goal is captured in plain language
- [ ] Ambiguities clarified (if goal vague → use Socratic Questioning)
- [ ] Constraints identified (timeline, technology stack, compatibility)
- [ ] Success criteria defined (what does "done" mean?)
- [ ] Read active `.github/memory.md` for prior context on similar work

---

## EXECUTION PROTOCOL

### 1. Goal Analysis

**Ask yourself:**
- What is the core problem being solved?
- What is the minimal viable solution?
- What foundational work must happen first?
- What can be deferred to later phases?

### 2. Phase Decomposition

**Each phase must:**
- **Achieve one clear objective** OR **enable the next phase**
- **Have distinct deliverable** (runnable code, test suite, data pipeline, etc.)
- **Build on previous phases** (no circular dependencies)
- **Be independently validatable** (can test/verify completion)

**Phase structure:**
```markdown
## Phase N: {Descriptive Name}

**Plan Summary:** {1-2 sentences: what gets built}

**Justification:** {Why this phase? Why this order? What does it enable?}
```

### 3. Self-Correction Gate

**For EACH phase, validate:**

❓ **"Does this phase directly achieve the goal or provide the required foundation for the next phase?"**

- **YES** → Phase is valid
- **NO** → Regenerate or merge with adjacent phase
- **UNCLEAR** → Phase is too abstract. Decompose further or clarify objective

**Common regeneration triggers:**
- Phase has no clear deliverable
- Phase duplicates work from another phase
- Phase can't be verified independently
- Phase doesn't connect to overall goal

---

## OUTPUT TEMPLATE

```markdown
# {Project Name} - Layer 1: Strategic Summary

**Goal:** {User's objective in 1-2 sentences}

**Success Criteria:** {How we know when done}

---

## Phase 1: {Name}

**Plan Summary:** {What gets built}

**Justification:** {Why first? What foundation does it provide?}

---

## Phase 2: {Name}

**Plan Summary:** {What gets built}

**Justification:** {Why after Phase 1? What does it enable?}

---

## Phase N: {Name}

**Plan Summary:** {What gets built}

**Justification:** {Why last? How does it complete the goal?}

---

**Next Steps:** Layer 2 will add operational granularity to each phase.
```

---

## COMMON PITFALLS

### ❌ AVOID: Phases that are too granular
**Bad:** "Phase 1: Import libraries | Phase 2: Define variables | Phase 3: Write function"  
**Good:** "Phase 1: Core data processing pipeline"

### ❌ AVOID: Technology-first thinking
**Bad:** "Phase 1: Set up React | Phase 2: Configure Redux"  
**Good:** "Phase 1: User authentication flow | Phase 2: Data visualization dashboard"

### ❌ AVOID: Phases without justification
**Bad:** "Phase 3: Add logging" (why? when? for what purpose?)  
**Good:** "Phase 3: Observability infrastructure - enables debugging production issues before Phase 4 deployment"

### ❌ AVOID: Monolithic phases
**Bad:** "Phase 1: Build entire application"  
**Good:** "Phase 1: Core data model | Phase 2: API layer | Phase 3: UI components | Phase 4: Integration"

### ❌ AVOID: Premature optimization
**Bad:** "Phase 1: High-performance caching layer"  
**Good:** "Phase 1: Basic data retrieval | Phase 2: Performance profiling | Phase 3: Optimization based on metrics"

---

## QUALITY GATES

**Before presenting Layer 1 to user:**

✅ **Completeness:** All phases cover the full scope of the user's goal  
✅ **Clarity:** Each phase has specific, understandable deliverable  
✅ **Justification:** Each phase explains WHY it exists and WHY its position in sequence  
✅ **Feasibility:** Each phase is achievable in reasonable scope (not too massive, not too trivial)  
✅ **Dependency Flow:** Phases build logically (1→2→3, not circular)  
✅ **Validation Path:** Each phase can be tested/verified independently  

**If any gate fails → regenerate before user review**

---

## ANTI-PATTERNS TO DETECT

🚫 **"Boil the Ocean"** - Phases too large, trying to do everything at once  
🚫 **"Premature Abstraction"** - Building reusable frameworks before solving core problem  
🚫 **"Technology Tourism"** - Phases focused on learning/using tools vs. solving problem  
🚫 **"Dependency Hell"** - Phase N requires Phase N+2 to work  
🚫 **"Invisible Progress"** - Can't tell when phase is complete  

---

## SELF-CORRECTION EXAMPLES

### Example 1: Too Granular
**Initial:**
- Phase 1: Create database schema
- Phase 2: Write SQL queries
- Phase 3: Add error handling
- Phase 4: Test database

**Self-Corrected:**
- Phase 1: Data persistence layer (schema + queries + error handling + tests)
- Phase 2: Business logic integration

### Example 2: Missing Foundation
**Initial:**
- Phase 1: User dashboard UI
- Phase 2: Backend API

**Self-Corrected (after validation):**
- Phase 1: Data model & API contracts (foundation)
- Phase 2: Backend API implementation
- Phase 3: User dashboard UI (consumes API)

### Example 3: Unclear Justification
**Initial:**
- Phase 3: Add caching

**Self-Corrected:**
- Phase 3: Performance optimization layer - Profiling in Phase 2 showed 2s load times; caching reduces to <200ms, enabling real-time dashboard in Phase 4

---

## SIGN-OFF PROTOCOL

**Present Layer 1 to user with:**
1. Full phase breakdown
2. Clear goal restatement
3. Request for explicit sign-off: *"Does this strategic breakdown align with your vision? Any phases to add/remove/reorder?"*

**Wait for approval phrases:** "approved", "proceed", "looks good", "continue"

**Do NOT proceed to Layer 2 without sign-off**
