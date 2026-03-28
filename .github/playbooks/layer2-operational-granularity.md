# Layer 2 Playbook: Operational Granularity

**Purpose:** Transform each Layer 1 phase into exact, actionable tasks with zero-ambiguity roadmap. NO code yet—pure operational clarity.

---

## PRE-FLIGHT CHECKLIST

**Before starting Layer 2:**

- [ ] Layer 1 has user sign-off (all phases approved)
- [ ] Layer 1 file exists: `{project}_layer1_strategic.md`
- [ ] Each Phase has Plan Summary + Justification
- [ ] Understand dependencies between phases

**CRITICAL:** Process ONE phase at a time. Do not attempt all phases simultaneously.

---

## ITERATION PROTOCOL

### Phase-by-Phase Workflow

**For EACH Phase in Layer 1:**

1. **Open Layer 1 document** for inline editing
2. **Select ONE phase** to expand
3. **Add task breakdown** beneath that phase
4. **Present to user** for review
5. **Wait for sign-off** before moving to next phase
6. **Repeat** for next phase

**Token Management:** Processing one phase at a time maximizes context window for detailed reasoning.

---

## TASK DECOMPOSITION FRAMEWORK

### What is a "Task"?

A task is a **discrete unit of work** with:
- **Clear start condition:** "When X is ready, begin Y"
- **Clear end condition:** "Y is complete when Z exists/passes"
- **No code implementation:** Describes WHAT to build, not HOW
- **Verifiable outcome:** Can check if done

### Task Granularity Rules

**Too Coarse (BAD):**
- "Build data pipeline" ❌
- "Create API" ❌

**Too Fine (BAD):**
- "Import datetime library" ❌
- "Define variable named user_id" ❌

**Just Right (GOOD):**
- "Define data schema with required fields, types, validation rules" ✅
- "Create API endpoint contract: routes, request/response shapes, error codes" ✅

### Task Decomposition Pattern

For each Phase, ask:

1. **What artifacts must exist?** (schemas, contracts, configs, test fixtures)
2. **What components must be built?** (functions, classes, modules, services)
3. **What validations must pass?** (unit tests, integration tests, edge cases)
4. **What integrations are needed?** (APIs, databases, external services)
5. **What edge cases must be handled?** (errors, empty data, rate limits)

---

## ZERO-AMBIGUITY ROADMAP CHECKLIST

**For EACH task, verify:**

✅ **Specificity:** Task name clearly states WHAT gets built  
✅ **Scope Boundary:** Task has defined start AND end  
✅ **No Implementation:** Describes outcome, not code steps  
✅ **Dependencies Clear:** Lists what must exist before this task can start  
✅ **Acceptance Criteria:** States how to verify completion  
✅ **No Orphans:** Every task connects to phase deliverable  

**If any check fails → refine task before presenting**

---

## OUTPUT TEMPLATE (Inline Edit to Layer 1)

**Before:**
```markdown
## Phase 2: Data Processing Pipeline

**Plan Summary:** Build ETL pipeline for customer data

**Justification:** Provides clean data for Phase 3 analytics
```

**After Layer 2 expansion:**
```markdown
## Phase 2: Data Processing Pipeline

**Plan Summary:** Build ETL pipeline for customer data

**Justification:** Provides clean data for Phase 3 analytics

### Tasks:

#### Task 2.1: Define Data Schema
- **What:** Customer data model with fields, types, constraints
- **Includes:** ID, name, email, timestamps, validation rules
- **Acceptance:** Schema definition file exists, all required fields documented
- **Dependencies:** None

#### Task 2.2: Create Data Extraction Logic
- **What:** Extract customer records from source database
- **Includes:** Connection handling, query logic, error handling for connection failures
- **Acceptance:** Can retrieve sample dataset without errors
- **Dependencies:** Task 2.1 (schema must be defined)

#### Task 2.3: Implement Data Transformation Rules
- **What:** Clean and normalize extracted data per schema
- **Includes:** Type conversion, null handling, format standardization
- **Acceptance:** Sample data passes schema validation
- **Dependencies:** Task 2.1, Task 2.2

#### Task 2.4: Build Data Loading Mechanism
- **What:** Write transformed data to target storage
- **Includes:** Batch writing, duplicate detection, transaction handling
- **Acceptance:** Sample data persisted correctly in target
- **Dependencies:** Task 2.3

#### Task 2.5: Add Pipeline Error Handling
- **What:** Graceful failure recovery and logging
- **Includes:** Retry logic, error logging, partial failure handling
- **Acceptance:** Pipeline continues on single record failure, logs errors
- **Dependencies:** Tasks 2.2-2.4

#### Task 2.6: Create Pipeline Tests
- **What:** Unit and integration tests for pipeline
- **Includes:** Happy path, error cases, edge cases (empty data, malformed records)
- **Acceptance:** All tests pass, >80% code coverage
- **Dependencies:** Tasks 2.1-2.5

---

**Phase 2 Status:** Ready for Layer 3 technical blueprints
```

---

## TASK NAMING CONVENTIONS

**Format:** `Task {PhaseNumber}.{TaskNumber}: {Action Verb} {Component}`

**Examples:**
- Task 1.1: Define API contract
- Task 1.2: Create authentication middleware
- Task 2.1: Design database schema
- Task 2.2: Implement query builder
- Task 3.1: Build user dashboard layout
- Task 3.2: Add data visualization widgets

**Action Verbs:** Define, Create, Build, Implement, Add, Design, Configure, Integrate, Validate

---

## COMMON PITFALLS

### ❌ AVOID: Implementation details leaking in
**Bad:** "Task 2.1: Use pandas.read_csv() to load data"  
**Good:** "Task 2.1: Create data ingestion logic for CSV files"

### ❌ AVOID: Vague outcomes
**Bad:** "Task 1.3: Make it work"  
**Good:** "Task 1.3: Implement request validation with error messages for invalid inputs"

### ❌ AVOID: Missing dependencies
**Bad:** Tasks can run in any order  
**Good:** "Task 2.3 Dependencies: Task 2.1 (schema), Task 2.2 (data extraction)"

### ❌ AVOID: Unverifiable tasks
**Bad:** "Task 3.2: Improve performance"  
**Good:** "Task 3.2: Add caching layer - Acceptance: Response time <200ms for cached queries"

### ❌ AVOID: Mixing multiple concerns
**Bad:** "Task 1.1: Build API and database and tests"  
**Good:** "Task 1.1: Define API endpoints | Task 1.2: Design database schema | Task 1.3: Create test fixtures"

---

## DEPENDENCY PATTERNS

### Linear Dependencies
```
Task 1.1 → Task 1.2 → Task 1.3 → Task 1.4
```
Each task requires previous completion.

### Parallel Tasks
```
Task 2.1 ──┐
Task 2.2 ──┼→ Task 2.4
Task 2.3 ──┘
```
Tasks 2.1-2.3 can run simultaneously, all feed into 2.4.

### Convergent Dependencies
```
Task 3.1 (Frontend) ──┐
Task 3.2 (Backend)  ──┼→ Task 3.3 (Integration)
Task 3.3 (Tests)    ──┘
```
Multiple independent streams merge.

**Mark dependencies explicitly in each task description**

---

## ACCEPTANCE CRITERIA TEMPLATES

**For Data Tasks:**
- "Schema validates against sample data"
- "Query returns expected row count"
- "All required fields populated"

**For API Tasks:**
- "Endpoint responds with 200 for valid request"
- "Returns 400 with error message for invalid input"
- "Response matches OpenAPI contract"

**For UI Tasks:**
- "Component renders without errors"
- "All interactive elements functional"
- "Responsive across mobile/desktop breakpoints"

**For Integration Tasks:**
- "End-to-end flow completes successfully"
- "Error propagation works across services"
- "Rollback mechanism tested"

**For Test Tasks:**
- "Coverage >80% for critical paths"
- "All edge cases have test scenarios"
- "Tests run in <2 minutes"

---

## PHASE COMPLETION CRITERIA

**A phase is ready for Layer 3 when:**

✅ All tasks have clear descriptions  
✅ Dependencies are explicit  
✅ Acceptance criteria are verifiable  
✅ No ambiguous language ("handle things", "make better")  
✅ No implementation details (library names, code patterns)  
✅ Task granularity is consistent (not mixing high/low level)  

---

## SIGN-OFF PROTOCOL

**After expanding ONE phase:**

1. **Present expanded phase** to user
2. **Highlight:** Number of tasks, key dependencies, acceptance criteria
3. **Ask:** "Does this operational breakdown for Phase N capture all necessary work? Any tasks missing or unclear?"
4. **Wait for approval phrases:** "approved", "proceed", "looks good"
5. **Upon approval:** Move to next phase
6. **Repeat** until all phases expanded

**Do NOT proceed to Layer 3 until ALL phases have Layer 2 sign-off**

---

## ITERATIVE REFINEMENT EXAMPLE

### Initial Task (Too Vague)
❌ **Task 1.1: Set up authentication**

### After Questioning
**User clarification:** "JWT-based auth with email/password login"

### Refined Tasks
✅ **Task 1.1: Define authentication contract**
- **What:** Login endpoint specification (POST /auth/login)
- **Includes:** Request schema (email, password), response schema (JWT token), error codes
- **Acceptance:** OpenAPI spec document exists
- **Dependencies:** None

✅ **Task 1.2: Create user credential validation**
- **What:** Verify email/password against stored credentials
- **Includes:** Password hashing verification, account lockout on failures
- **Acceptance:** Returns true/false for valid/invalid credentials
- **Dependencies:** Task 1.1

✅ **Task 1.3: Implement JWT token generation**
- **What:** Generate signed JWT on successful login
- **Includes:** User ID in payload, expiration timestamp, signing with secret key
- **Acceptance:** Generated token validates with JWT library
- **Dependencies:** Task 1.2

✅ **Task 1.4: Add authentication middleware**
- **What:** Verify JWT on protected routes
- **Includes:** Token parsing, signature validation, expiration check
- **Acceptance:** Protected routes reject invalid/expired tokens
- **Dependencies:** Task 1.3

---

## ANTI-PATTERNS TO DETECT

🚫 **"The Wall of Tasks"** - 20+ tasks for single phase (phase too large, decompose further at Layer 1)  
🚫 **"Implementation Creep"** - Tasks specify code patterns/libraries instead of outcomes  
🚫 **"Dependency Spaghetti"** - Tasks have circular dependencies or unclear order  
🚫 **"Acceptance Amnesia"** - Tasks lack verification criteria ("how do we know it's done?")  
🚫 **"Scope Drift"** - Tasks go beyond phase deliverable ("nice to have" features)  

---

## CONTEXT WINDOW OPTIMIZATION

**Why one phase at a time?**

When expanding Phase 3 of 5:
- **Full Layer 1 context:** Maintains awareness of overall plan
- **Deep Phase 3 focus:** Maximum tokens for task decomposition
- **No Phase 4/5 noise:** Irrelevant future phases excluded from reasoning

**Benefit:** Can add 10-15 detailed tasks per phase without token overflow, vs. 3-5 tasks if processing all phases simultaneously.
