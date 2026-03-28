# Decision Tree: Architecture Choices

**Purpose:** Systematic decision logic for resolving architectural ambiguities during implementation.

**When to Load:** When encountering architectural choice unclear during Layer 3 (Technical Blueprints) or Layer 4 (DRY Audit).

---

## DECISION 1: HELPER FUNCTION vs INLINE

**Scenario:** Code block could be extracted to helper function OR left inline.

### Decision Flowchart

```
START: Code block identified
    ↓
Q1: Is block used in multiple places?
    ├─ YES → Extract to helper function
    └─ NO → Continue to Q2
         ↓
Q2: Is block >10 lines?
    ├─ YES → Continue to Q3
    └─ NO → Continue to Q3
         ↓
Q3: Does block have single clear responsibility?
    ├─ YES → Continue to Q4
    └─ NO → Keep INLINE (mixed concerns, can't name clearly)
         ↓
Q4: Can you name it without using "and" or "or"?
    ├─ YES → Continue to Q5
    └─ NO → Keep INLINE (violates Single Responsibility)
         ↓
Q5: Does extraction improve readability?
    ├─ YES → Extract to helper function
    └─ NO → Keep INLINE
```

### Rules

**EXTRACT when:**
- ✅ Used in ≥2 places (DRY principle)
- ✅ Complex logic that benefits from isolation
- ✅ Clear single responsibility
- ✅ Can be unit tested independently
- ✅ Name clearly communicates purpose

**KEEP INLINE when:**
- ✅ Used once only
- ✅ <10 lines AND simple logic
- ✅ Tightly coupled to parent function context
- ✅ Extraction would require passing 5+ parameters
- ✅ No clear name possible without using "and"

### Examples

**Case 1: Extract**

```python
# BEFORE (inline)
def process_order(order):
    # Validate order
    if not order.get('id'):
        raise ValueError("Missing order ID")
    if not order.get('items'):
        raise ValueError("Missing order items")
    if order.get('total', 0) <= 0:
        raise ValueError("Invalid order total")
    
    # Process payment
    # ... (more code)
```

**AFTER (extracted):**

```python
def validate_order(order):
    """Validate order has required fields."""
    if not order.get('id'):
        raise ValueError("Missing order ID")
    if not order.get('items'):
        raise ValueError("Missing order items")
    if order.get('total', 0) <= 0:
        raise ValueError("Invalid order total")

def process_order(order):
    validate_order(order)
    # Process payment
    # ... (more code)
```

**Why:** Clear responsibility (validation), reusable, testable, improves readability.

---

**Case 2: Keep Inline**

```python
# This is fine as-is
def calculate_discount(price, customer_tier):
    # Apply tier multiplier
    multiplier = 0.9 if customer_tier == 'gold' else 0.95
    return price * multiplier
```

**Why NOT extract `0.9 if ... else 0.95`:**
- Single use
- 1 line, trivial
- Extraction adds no value
- Name would be verbose: `get_discount_multiplier_for_tier()`

---

## DECISION 2: ABSTRACTION vs DUPLICATION

**Scenario:** Similar code exists in multiple places. Abstract into shared function OR keep duplicated.

### Decision Flowchart

```
START: Similar code in N places
    ↓
Q1: Is code IDENTICAL or just SIMILAR?
    ├─ IDENTICAL → Continue to Q2
    └─ SIMILAR → Continue to Q3
         ↓
Q2: Will all instances evolve together?
    ├─ YES → Abstract (shared fate)
    └─ NO → Keep DUPLICATED (independent evolution)
         ↓
Q3: How many parameters needed for abstraction?
    ├─ ≤3 params → Continue to Q4
    └─ >3 params → Keep DUPLICATED (too many coupling points)
         ↓
Q4: Does abstraction reduce total lines >30%?
    ├─ YES → Abstract
    └─ NO → Keep DUPLICATED (overhead not justified)
```

### Rules

**ABSTRACT when:**
- ✅ Code is IDENTICAL across ≥3 places
- ✅ Shared evolution (changes apply to all instances)
- ✅ Abstraction ≤3 parameters
- ✅ Reduces code by >30%
- ✅ Clear name captures shared concept

**KEEP DUPLICATED when:**
- ✅ Code is SIMILAR but not identical
- ✅ Instances likely to diverge (different evolution paths)
- ✅ Abstraction requires >3 parameters (high coupling)
- ✅ Reduction <30% (not worth complexity)
- ✅ Only 2 instances (premature abstraction)

### Examples

**Case 1: Abstract**

```python
# BEFORE (duplicated)
def validate_email(email):
    if not email or '@' not in email:
        raise ValueError("Invalid email")

def validate_phone(phone):
    if not phone or len(phone) < 10:
        raise ValueError("Invalid phone")

def validate_zip(zip_code):
    if not zip_code or len(zip_code) != 5:
        raise ValueError("Invalid zip")
```

**AFTER (abstracted):**

```python
def validate_field(value, validator_fn, error_msg):
    """Generic field validation."""
    if not value or not validator_fn(value):
        raise ValueError(error_msg)

def validate_email(email):
    validate_field(email, lambda e: '@' in e, "Invalid email")

def validate_phone(phone):
    validate_field(phone, lambda p: len(p) >= 10, "Invalid phone")

def validate_zip(zip_code):
    validate_field(zip_code, lambda z: len(z) == 5, "Invalid zip")
```

**Why:** Identical pattern (check + raise), shared evolution (validation rules stable), ≤3 params.

---

**Case 2: Keep Duplicated**

```python
# BEFORE (similar)
def process_payment(amount):
    logger.info(f"Processing payment: ${amount}")
    # Payment-specific logic
    db.save_payment(amount)
    notify_accounting(amount)

def process_refund(amount):
    logger.info(f"Processing refund: ${amount}")
    # Refund-specific logic
    db.save_refund(amount)
    notify_customer(amount)
```

**DON'T abstract:**

```python
# WRONG - forced abstraction
def process_transaction(amount, type, save_fn, notify_fn):
    logger.info(f"Processing {type}: ${amount}")
    save_fn(amount)
    notify_fn(amount)
```

**Why keep duplicated:**
- Similar structure but different semantics
- Likely to diverge (different business rules)
- Abstraction requires 4 params (high coupling)
- Reduces clarity (what is a "transaction"?)

---

## DECISION 3: PATTERN SELECTION

**Scenario:** Need to choose design pattern for implementation.

### Factory vs Builder vs Direct Instantiation

```
START: Need to create objects
    ↓
Q1: Creation logic complex (>3 parameters OR conditional logic)?
    ├─ NO → Direct Instantiation
    └─ YES → Continue to Q2
         ↓
Q2: Need to build object step-by-step?
    ├─ YES → Builder Pattern
    └─ NO → Continue to Q3
         ↓
Q3: Multiple object types created based on input?
    ├─ YES → Factory Pattern
    └─ NO → Direct Instantiation (with helper)
```

**Direct Instantiation:** Simple creation, ≤3 params, no conditional logic

```python
validator = EmailValidator(regex_pattern, allow_plus=True)
```

**Factory Pattern:** Multiple types, selection based on input

```python
def create_validator(type: str) -> Validator:
    if type == 'email':
        return EmailValidator()
    elif type == 'phone':
        return PhoneValidator()
    # ...
```

**Builder Pattern:** Complex construction, many optional params

```python
validator = (ValidatorBuilder()
    .with_email_check()
    .with_length_constraint(min=5, max=100)
    .with_custom_rule(my_rule)
    .build())
```

---

### Strategy vs Template Method vs Plain Functions

```
START: Need interchangeable algorithms
    ↓
Q1: Algorithms share common structure?
    ├─ YES → Continue to Q2
    └─ NO → Strategy Pattern
         ↓
Q2: Structure has ≥3 fixed steps?
    ├─ YES → Template Method Pattern
    └─ NO → Plain Functions
```

**Plain Functions:** Simple algorithm swap, no shared structure

```python
def process(data, algorithm_fn):
    return algorithm_fn(data)

result = process(data, fast_algorithm)
```

**Strategy Pattern:** Complex algorithms, runtime selection, some shared code

```python
class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data): pass

class StrictValidator(ValidationStrategy):
    def validate(self, data):
        # Strict logic
```

**Template Method:** Fixed process with variable steps

```python
class DataProcessor(ABC):
    def process(self, data):  # Template
        self.validate(data)
        self.transform(data)
        self.save(data)
    
    @abstractmethod
    def transform(self, data):  # Override point
        pass
```

---

### Decorator vs Inheritance vs Composition

```
START: Need to extend behavior
    ↓
Q1: Extension optional/runtime?
    ├─ YES → Continue to Q2
    └─ NO → Inheritance
         ↓
Q2: Need multiple independent extensions?
    ├─ YES → Decorator Pattern
    └─ NO → Composition
```

**Inheritance:** Extension is permanent, single path

```python
class BaseValidator:
    def validate(self, data): pass

class EmailValidator(BaseValidator):  # IS-A relationship
    def validate(self, data):
        # Email-specific
```

**Composition:** Extension is permanent, multiple capabilities

```python
class Validator:
    def __init__(self, rule_checker, error_handler):
        self.rule_checker = rule_checker  # HAS-A
        self.error_handler = error_handler
```

**Decorator:** Extension is optional/runtime, stackable

```python
@cache_results
@log_calls
@retry_on_failure
def validate(data):
    # Core logic
```

---

## DECISION 4: SINGLE FUNCTION vs CLASS

**Scenario:** Should functionality be a function or a class?

### Decision Flowchart

```
START: Need to implement functionality
    ↓
Q1: Does it maintain state between calls?
    ├─ YES → Class
    └─ NO → Continue to Q2
         ↓
Q2: Does it have ≥3 related methods?
    ├─ YES → Class
    └─ NO → Continue to Q3
         ↓
Q3: Does it need initialization/configuration?
    ├─ YES → Class
    └─ NO → Function
```

### Rules

**USE CLASS when:**
- ✅ Maintains state between calls
- ✅ ≥3 related methods that share data
- ✅ Needs initialization/configuration
- ✅ Represents a real-world entity/concept
- ✅ Benefits from inheritance or polymorphism

**USE FUNCTION when:**
- ✅ Stateless transformation
- ✅ Single responsibility
- ✅ No initialization needed
- ✅ Pure function (same input → same output)

### Examples

**Case 1: Use Function**

```python
# Stateless transformation
def validate_email(email: str) -> bool:
    return '@' in email and '.' in email.split('@')[1]
```

**Case 2: Use Class**

```python
# Maintains state (registered rules)
class Validator:
    def __init__(self):
        self.rules = []
    
    def register_rule(self, rule):
        self.rules.append(rule)
    
    def validate(self, data):
        return all(rule(data) for rule in self.rules)
```

---

## DECISION 5: EXCEPTION vs RETURN CODE

**Scenario:** How to signal errors?

### Decision Flowchart

```
START: Need to signal error condition
    ↓
Q1: Is error recoverable by caller?
    ├─ NO → Exception (exceptional condition)
    └─ YES → Continue to Q2
         ↓
Q2: Is error expected/common?
    ├─ YES → Return code (normal flow)
    └─ NO → Exception (exceptional condition)
```

### Rules

**USE EXCEPTION when:**
- ✅ Unrecoverable error (file not found, network failure)
- ✅ Unexpected condition (invariant violated)
- ✅ Caller can't reasonably check before calling
- ✅ Error should propagate up call stack

**USE RETURN CODE when:**
- ✅ Expected outcome (validation failure on user input)
- ✅ Caller expected to handle immediately
- ✅ Error is common in normal operation
- ✅ Error is part of API contract

### Examples

**Case 1: Exception**

```python
def read_config(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config not found: {filepath}")
    # ...
```

**Why:** File missing is exceptional, unrecoverable without intervention.

---

**Case 2: Return Code**

```python
def validate_user_input(data) -> ValidationResult:
    if not data.get('email'):
        return ValidationResult(valid=False, error="Missing email")
    # ...
    return ValidationResult(valid=True)
```

**Why:** Validation failure is expected, caller handles in normal flow.

---

## DECISION 6: SYNC vs ASYNC

**Scenario:** Should function be synchronous or asynchronous?

### Decision Flowchart

```
START: Implementing function
    ↓
Q1: Does it perform I/O (network, disk, database)?
    ├─ YES → Continue to Q2
    └─ NO → Sync
         ↓
Q2: Is I/O operation >50ms typical latency?
    ├─ YES → Continue to Q3
    └─ NO → Sync (overhead not justified)
         ↓
Q3: Are there ≥5 calls that could run concurrently?
    ├─ YES → Async
    └─ NO → Continue to Q4
         ↓
Q4: Is caller already async?
    ├─ YES → Async (fit ecosystem)
    └─ NO → Sync (keep simple)
```

### Rules

**USE ASYNC when:**
- ✅ I/O-bound operations >50ms
- ✅ Multiple concurrent operations possible
- ✅ Part of async ecosystem (event loop already running)
- ✅ Need high concurrency (thousands of requests)

**USE SYNC when:**
- ✅ CPU-bound operations
- ✅ Fast I/O (<50ms)
- ✅ Sequential processing required
- ✅ Simpler codebase (no event loop needed)

---

## QUICK REFERENCE TABLE

| Decision | Choose A | Choose B | Key Factor |
|----------|----------|----------|------------|
| **Helper vs Inline** | Extract | Inline | Used ≥2 places OR >10 lines + clear responsibility |
| **Abstract vs Duplicate** | Abstract | Duplicate | Identical + shared evolution + ≤3 params + >30% reduction |
| **Factory vs Builder** | Factory | Builder | Multiple types vs Step-by-step construction |
| **Strategy vs Template** | Strategy | Template | No shared structure vs ≥3 fixed steps |
| **Function vs Class** | Function | Class | Stateless + single method vs Stateful + ≥3 methods |
| **Exception vs Return** | Exception | Return code | Exceptional/unrecoverable vs Expected/recoverable |
| **Sync vs Async** | Sync | Async | Fast (<50ms) vs Slow I/O + concurrency |

---

## USAGE IN CCE WORKFLOW

**Layer 3 (Technical Blueprints):**
- Load when architectural choice has no clear answer
- Apply decision flowchart
- Document choice rationale in Layer 1

**Layer 4 (DRY Audit):**
- Use "Abstract vs Duplicate" decision tree
- Use "Helper vs Inline" for consolidation candidates
- Quantify gains (30% threshold)

**Cross-Reference:**
- If still ambiguous after decision tree → Load `.github/exploits/socratic-questioning.md`
- Present options to user with trade-offs from decision tree
