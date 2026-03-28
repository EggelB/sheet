# Layer 4 Playbook: DRY Audit & Consolidation

**Purpose:** Mandatory minimalist review of Layer 3 blueprints to eliminate redundancy, optimize algorithms, and reduce code complexity before implementation.

---

## PRE-FLIGHT CHECKLIST

**Before starting Layer 4:**

- [ ] All Layer 3 phase blueprints complete with user sign-off
- [ ] All functions have full implementations (not pseudocode)
- [ ] Read entire Layer 3 document to understand full codebase
- [ ] Identify cross-phase patterns (same logic in multiple phases)

**Mindset:** Your job is to challenge every abstraction. Ask: "Does this reduce complexity or add indirection?"

---

## RED FLAG DETECTION CHECKLIST

Scan ALL Layer 3 blueprints for these patterns:

### 🚩 Category 1: Trivial Wrappers

**Pattern:** Functions <5 lines that only call another function

**Example (RED FLAG):**
```python
def get_customer(customer_id: str) -> Customer:
    """Get customer by ID."""
    return repository.get_by_id(customer_id)

def fetch_customer(customer_id: str) -> Customer:
    """Fetch customer by ID."""
    return repository.get_by_id(customer_id)
```

**Consolidation:**
```python
# DELETE both wrappers. Call repository.get_by_id() directly at usage sites.
# OR if wrapper adds value, keep ONE with better name and delete the other
```

**Detection Questions:**
- Is function body just `return other_function(params)`?
- Does function add validation, logging, or transformation? (If NO → DELETE)
- Are there 2+ functions wrapping the same target? (Merge to ONE)

---

### 🚩 Category 2: Identical Logic Duplication

**Pattern:** 2+ functions with identical or near-identical logic on same data

**Example (RED FLAG):**
```python
def filter_active_customers(customers: List[Customer]) -> List[Customer]:
    """Get active customers."""
    return [c for c in customers if c.status == 'active']

def get_active_customers(customers: List[Customer]) -> List[Customer]:
    """Return active customers."""
    return [c for c in customers if c.status == 'active']

def find_active_users(customers: List[Customer]) -> List[Customer]:
    """Find active users."""
    return [c for c in customers if c.status == 'active']
```

**Consolidation:**
```python
def filter_by_status(
    customers: List[Customer],
    status: str = 'active'
) -> List[Customer]:
    """
    Filter customers by status.
    
    Args:
        customers: List of customer objects
        status: Status to filter by (default: 'active')
    
    Returns:
        Filtered list of customers matching status
    """
    return [c for c in customers if c.status == status]

# DELETE the other 2-3 functions. Replace all call sites with filter_by_status()
```

**Detection Questions:**
- Do functions iterate same data structure?
- Do they apply identical filtering/transformation logic?
- Could ONE parameterized function replace N variants?

---

### 🚩 Category 3: Sequential Iterations (Multi-Pass)

**Pattern:** Multiple O(n) iterations over same dataset that could be single-pass

**Example (RED FLAG):**
```python
def process_orders(orders: List[Order]) -> ProcessResult:
    """Process orders with validation and transformation."""
    
    # Pass 1: Validate
    validated = []
    for order in orders:
        if order.total > 0:
            validated.append(order)
    
    # Pass 2: Transform
    transformed = []
    for order in validated:
        transformed.append(order.total * 1.1)  # Add tax
    
    # Pass 3: Sum
    total = 0
    for price in transformed:
        total += price
    
    return ProcessResult(total=total, count=len(validated))
```

**Consolidation (Single-Pass O(n)):**
```python
def process_orders(orders: List[Order]) -> ProcessResult:
    """
    Process orders with validation, transformation, and aggregation.
    
    Performs validation, tax calculation, and summation in single pass.
    """
    total = 0
    valid_count = 0
    
    for order in orders:
        # Validate
        if order.total <= 0:
            continue
        
        # Transform and accumulate
        taxed_price = order.total * 1.1
        total += taxed_price
        valid_count += 1
    
    return ProcessResult(total=total, count=valid_count)
```

**Efficiency Gain:** 3×O(n) → 1×O(n) = **67% reduction in iterations**

**Detection Questions:**
- Are there multiple `for` loops over same dataset?
- Can transformations happen during single iteration?
- Can aggregation happen inline instead of separate pass?

---

### 🚩 Category 4: Thin Orchestration

**Pattern:** Functions that only call 2-3 other functions in sequence without logic

**Example (RED FLAG):**
```python
def create_customer_workflow(data: Dict) -> Customer:
    """Create customer workflow."""
    validated = validate_customer_data(data)
    customer = build_customer_object(validated)
    saved = save_to_database(customer)
    return saved
```

**Consolidation:**
```python
# DELETE create_customer_workflow()
# At call site, inline the sequence:
validated = validate_customer_data(data)
customer = build_customer_object(validated)
saved = save_to_database(customer)

# OR if orchestration is complex business logic, keep it.
# But if it's just A→B→C with no branching/error handling, inline it.
```

**Detection Questions:**
- Does function contain branching logic or error handling? (If NO → inline)
- Is sequence called from multiple places? (If YES → keep function)
- Does orchestration encapsulate important business process? (Judgment call)

---

### 🚩 Category 5: Premature Abstraction

**Pattern:** Generic utility functions used only once or overcomplicated for actual use

**Example (RED FLAG):**
```python
def apply_transformation(
    data: Any,
    transform_fn: Callable,
    filter_fn: Optional[Callable] = None,
    aggregator: Optional[Callable] = None
) -> Any:
    """Flexible transformation pipeline."""
    # 50 lines of generic pipeline logic
    pass

# Used only once:
result = apply_transformation(
    customers,
    lambda c: c.name.upper(),
    lambda c: c.active,
    lambda results: len(results)
)
```

**Consolidation:**
```python
# DELETE apply_transformation(). Replace with direct logic:
active_count = len([c.name.upper() for c in customers if c.active])

# Simpler, clearer, no indirection
```

**Detection Questions:**
- Is "flexible" function used only 1-2 times?
- Does abstraction make code harder to understand?
- Would inline code be clearer than callback-heavy abstraction?

---

## ALGORITHMIC EFFICIENCY ANALYSIS

### Time Complexity Opportunities

**Scan for these patterns:**

#### O(n²) → O(n log n) or O(n)

**Bad:**
```python
def find_duplicates(items: List[str]) -> List[str]:
    """Find duplicate items."""
    duplicates = []
    for i, item in enumerate(items):
        for j, other in enumerate(items):
            if i != j and item == other and item not in duplicates:
                duplicates.append(item)
    return duplicates
```

**Good:**
```python
def find_duplicates(items: List[str]) -> List[str]:
    """Find duplicate items."""
    from collections import Counter
    counts = Counter(items)
    return [item for item, count in counts.items() if count > 1]
```

**Gain:** O(n²) → O(n)

---

#### Multiple Lookups → Hash Table

**Bad:**
```python
def enrich_orders(orders: List[Order], customers: List[Customer]) -> List[EnrichedOrder]:
    """Add customer data to orders."""
    enriched = []
    for order in orders:
        # O(n) lookup per order = O(n²) total
        customer = next((c for c in customers if c.id == order.customer_id), None)
        enriched.append(EnrichedOrder(order, customer))
    return enriched
```

**Good:**
```python
def enrich_orders(orders: List[Order], customers: List[Customer]) -> List[EnrichedOrder]:
    """Add customer data to orders."""
    # Build hash table: O(n)
    customer_map = {c.id: c for c in customers}
    
    # Lookup per order: O(1) × n orders = O(n) total
    enriched = [
        EnrichedOrder(order, customer_map.get(order.customer_id))
        for order in orders
    ]
    return enriched
```

**Gain:** O(n²) → O(n)

---

#### Unnecessary Sorting → Streaming Min/Max

**Bad:**
```python
def get_top_5_customers(customers: List[Customer]) -> List[Customer]:
    """Get top 5 customers by revenue."""
    sorted_customers = sorted(customers, key=lambda c: c.revenue, reverse=True)
    return sorted_customers[:5]
```

**Good (if n is large):**
```python
import heapq

def get_top_5_customers(customers: List[Customer]) -> List[Customer]:
    """Get top 5 customers by revenue."""
    return heapq.nlargest(5, customers, key=lambda c: c.revenue)
```

**Gain:** O(n log n) → O(n log k) where k=5

---

### Space Complexity Opportunities

**Scan for:**

#### Unnecessary Copies

**Bad:**
```python
def process_data(data: List) -> List:
    """Process data."""
    copy1 = data.copy()
    copy2 = [x for x in copy1]
    copy3 = list(copy2)
    return [transform(x) for x in copy3]
```

**Good:**
```python
def process_data(data: List) -> List:
    """Process data."""
    return [transform(x) for x in data]
```

#### Streaming vs. Materialization

**Bad (materializes all intermediate results):**
```python
def process_large_dataset(items: Iterator) -> int:
    """Process large dataset."""
    filtered = [x for x in items if x.valid]
    transformed = [transform(x) for x in filtered]
    return sum(transformed)
```

**Good (streaming):**
```python
def process_large_dataset(items: Iterator) -> int:
    """Process large dataset."""
    return sum(transform(x) for x in items if x.valid)
```

**Gain:** O(n) space → O(1) space

---

## QUANTIFICATION FRAMEWORK

**For EVERY consolidation recommendation, provide:**

### Metric 1: Function Reduction

**Template:**
```
BEFORE: 15 functions
AFTER: 9 functions
REDUCTION: 6 functions removed (40% reduction)
```

### Metric 2: Iteration Reduction

**Template:**
```
BEFORE: 5 iterations over customers list (5×O(n))
AFTER: 1 iteration over customers list (1×O(n))
IMPROVEMENT: 80% fewer iterations
```

### Metric 3: Complexity Improvement

**Template:**
```
BEFORE: O(n²) nested loops for duplicate detection
AFTER: O(n) using hash table
IMPROVEMENT: n=1000 → 1,000,000 ops to 1,000 ops (99.9% reduction)
```

### Metric 4: Lines of Code

**Template:**
```
BEFORE: 250 lines across 12 functions
AFTER: 180 lines across 7 functions
REDUCTION: 70 lines removed (28% reduction), 5 functions consolidated
```

---

## CONSOLIDATION RECOMMENDATION TEMPLATE

**Format for presenting to user:**

```markdown
## Layer 4 DRY Audit Results

### Summary
- **Functions Analyzed:** 42
- **Red Flags Detected:** 8
- **Consolidation Opportunities:** 5
- **Estimated Reduction:** 35% fewer functions, 40% fewer iterations

---

### Consolidation 1: Merge Customer Filter Functions

**Current State:**
- `filter_active_customers()` - 8 lines
- `get_active_customers()` - 8 lines  
- `find_active_users()` - 8 lines

**Issue:** Identical logic duplicated 3 times

**Proposed Solution:**
Create single parameterized function: `filter_customers_by_status(customers, status='active')`

**Impact:**
- Delete 3 functions → 1 function (67% reduction)
- Eliminate 16 lines of duplicate code
- Future status filters reuse same function

**User Decision:** Approve consolidation? [Yes/No]

---

### Consolidation 2: Inline Order Processing Orchestration

**Current State:**
- `process_order_workflow()` - 5 lines
  - Calls `validate()` → `transform()` → `save()`
  - No branching, error handling, or business logic

**Issue:** Thin orchestration wrapper adds indirection without value

**Proposed Solution:**
Delete `process_order_workflow()`, inline 3-step sequence at call sites

**Impact:**
- Remove 1 unnecessary abstraction
- 5 lines deleted
- Clearer code flow (no jumping through wrapper)

**User Decision:** Approve consolidation? [Yes/No]

---

### Efficiency Improvement 1: Single-Pass Order Processing

**Current State:**
- Pass 1: Validate orders (iterate all)
- Pass 2: Transform orders (iterate validated)
- Pass 3: Sum totals (iterate transformed)
- **Total:** 3×O(n) = approximately 3n iterations

**Issue:** Multiple passes over same dataset

**Proposed Solution:**
Combine validation, transformation, summation into single loop

**Impact:**
- 3×O(n) → 1×O(n)
- For 10,000 orders: 30,000 iterations → 10,000 iterations (67% reduction)
- Lower memory footprint (no intermediate lists)

**User Decision:** Approve optimization? [Yes/No]
```

---

## CONSOLIDATION DECISION TREE

```
For each detected red flag:

├─ Category 1: Trivial Wrapper
│  ├─ Does wrapper add validation/logging/transformation?
│  │  ├─ YES → Keep wrapper (adds value)
│  │  └─ NO → DELETE wrapper, call target directly
│  └─ Are there multiple wrappers to same target?
│     └─ YES → Keep best ONE, delete others

├─ Category 2: Duplicate Logic
│  ├─ Can functions be unified with parameters?
│  │  ├─ YES → Create parameterized function, delete variants
│  │  └─ NO → Keep separate (different business contexts)
│  └─ Are there >2 duplicates?
│     └─ YES → Consolidation priority HIGH

├─ Category 3: Multi-Pass Iteration
│  ├─ Can logic be combined into single pass?
│  │  ├─ YES → Consolidate to single loop
│  │  └─ NO → Keep separate (dependencies prevent merge)
│  └─ Is dataset >1000 items?
│     └─ YES → Optimization priority HIGH

├─ Category 4: Thin Orchestration
│  ├─ Does function have branching/error handling?
│  │  ├─ YES → Keep (non-trivial logic)
│  │  └─ NO → Consider inlining
│  ├─ Is sequence called from multiple places?
│  │  ├─ YES → Keep function (DRY principle)
│  │  └─ NO → Inline at call site
│  └─ Does orchestration represent business process?
│     └─ YES → Keep (semantic value)

└─ Category 5: Premature Abstraction
   ├─ Is abstraction used >2 times?
   │  ├─ YES → Keep (reuse justifies complexity)
   │  └─ NO → Delete, replace with direct code
   └─ Does abstraction improve clarity?
      ├─ YES → Keep (readability value)
      └─ NO → Delete (indirection without benefit)
```

---

## ANTI-PATTERNS TO PRESERVE

**NOT everything should be consolidated. Keep these patterns:**

### ✅ Intentional Duplication (Domain Separation)

```python
# Customer domain
def validate_customer_email(email: str) -> bool:
    """Validate customer email per customer rules."""
    return '@' in email and len(email) > 5

# Employee domain  
def validate_employee_email(email: str) -> bool:
    """Validate employee email per employee rules."""
    return '@company.com' in email
```

**Why Keep:** Different business domains, may diverge in future

---

### ✅ Semantic Wrappers (Improve Readability)

```python
def is_customer_eligible_for_discount(customer: Customer) -> bool:
    """Check if customer qualifies for discount."""
    return customer.orders > 10 and customer.total_spent > 1000

# More readable than:
# if customer.orders > 10 and customer.total_spent > 1000:
```

**Why Keep:** Encapsulates business rule, improves code readability

---

### ✅ Interface Compliance

```python
class CustomerRepository:
    def get_by_id(self, id: str) -> Customer:
        """Get customer by ID."""
        return self.db.get_customer(id)  # Thin wrapper

# Implements Repository interface contract
```

**Why Keep:** Satisfies interface/protocol requirement

---

## EXECUTION PROTOCOL

### Step 1: Full Scan

Read all Layer 3 blueprints. Create inventory:
- Total functions count
- Functions per category (data access, business logic, utilities, etc.)
- Identify all potential red flags

### Step 2: Categorize Red Flags

Group detected issues by category:
- Trivial wrappers: [list]
- Duplicate logic: [list]
- Multi-pass: [list]
- Thin orchestration: [list]
- Premature abstraction: [list]

### Step 3: Quantify Impact

For each consolidation opportunity, calculate:
- Function count reduction
- Iteration reduction
- Complexity improvement
- Lines of code reduction

### Step 4: Present Recommendations

Format findings per template above. Present to user with:
- Summary metrics
- Individual consolidation proposals
- Quantified gains
- Request for approval per item

### Step 5: Wait for Approval

**CRITICAL:** Do NOT execute consolidations without explicit user approval

User may reject some consolidations for business reasons you're unaware of.

### Step 6: Execute Approved Consolidations

Only after user approves specific consolidations:
- Update Layer 3 blueprints
- Remove consolidated functions
- Update remaining functions with optimizations
- Mark completed consolidations

---

## SIGN-OFF PROTOCOL

**Present audit results:**
1. **Summary metrics** (functions analyzed, red flags, estimated reduction)
2. **Detailed consolidations** (one per section, with quantified gains)
3. **Ask:** "Which consolidations should I execute? Approve all, specific ones, or none?"
4. **Wait for specific approval** per consolidation or batch approval
5. **Execute only approved items**
6. **Present updated Layer 3** after consolidations

**Do NOT proceed to Layer 5 without completing approved consolidations**

---

## QUALITY GATES

**Before presenting audit:**

✅ **Completeness:** All Layer 3 blueprints scanned  
✅ **Quantification:** Every recommendation has metrics  
✅ **Justification:** Each consolidation explains WHY and impact  
✅ **Clarity:** Recommendations show BEFORE/AFTER code  
✅ **Prioritization:** High-impact items listed first  
✅ **Conservative:** Not flagging intentional patterns (domain separation, semantic wrappers)  

**If any gate fails → refine audit before presenting**
