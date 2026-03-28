# Layer 3 Playbook: Technical Blueprints

**Purpose:** Generate structural blueprints — type-annotated signatures, dataclasses, docstrings, and **rudimentary guidance logic** sufficient to direct the Developer. Process ONE phase at a time.

> **Layer 3 is a specification step, not an implementation step.** Full production implementation is the Developer's role, executed after Layer 4 DRY audit and Layer 5 Pure Signal brief. Layer 3 output must be above pseudocode (no bare `pass`/TODO stubs) but is not required to be production-complete.

---

## PRE-FLIGHT CHECKLIST

**Before starting Layer 3:**

- [ ] Layer 2 has user sign-off for ALL phases
- [ ] All tasks have acceptance criteria defined
- [ ] Dependencies between tasks are clear
- [ ] **CRITICAL:** Load `.github/exploits/context-gating.md` and apply optimization
- [ ] **CRITICAL:** Load `.github/exploits/skeleton-of-thought.md` for implementation strategy

**Context Optimization (from Context Gating):**

- Close irrelevant editor tabs
- Exclude `node_modules/`, `dist/`, `.git/`, `build/`, `__pycache__/` from workspace
- Focus only on current phase being implemented

---

## SKELETON-FIRST METHODOLOGY

**NEVER write full implementations immediately. Always follow this sequence:**

### Step 1: Extract Structural Components

For the current phase, identify:

- **Interfaces/Protocols:** What contracts must be defined?
- **Type Definitions:** What custom types/classes are needed?
- **Function Signatures:** What are the function names, parameters, return types?
- **Constants/Enums:** What configuration values exist?

### Step 2: Generate Skeleton

Create structure WITHOUT implementation:

```python
# Example Skeleton
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Customer:
    """Customer data model."""
    id: str
    name: str
    email: str
    created_at: datetime

class CustomerRepository:
    """Handles customer data persistence."""
  
    def __init__(self, connection_string: str):
        """Initialize repository with database connection."""
        pass
  
    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        """Retrieve customer by ID."""
        pass
  
    def create(self, customer: Customer) -> Customer:
        """Create new customer record."""
        pass
  
    def update(self, customer: Customer) -> Customer:
        """Update existing customer."""
        pass
```

### Step 3: User Review of Skeleton

**STOP and present skeleton to user:**

- "Here's the structural blueprint for Phase N. Does this architecture align with your expectations?"
- Wait for explicit approval before filling in implementations

### Step 4: Add Guidance Logic

Only AFTER skeleton approval, add **rudimentary logic** to each function — enough to communicate the intended call structure, branching, and data transformations to the Developer. This is a specification aid, not production-complete code. Edge-case handling, performance tuning, and defensive hardening are the Developer's responsibility in Layer 6 (post-Layer 5 handoff).

---

## IMPLEMENTATION STANDARDS

### Function Signature Requirements

**Every function MUST have:**

1. **Type Hints** (parameters and return)
2. **Docstring** (see templates below)
3. **Parameter Validation** (if applicable)
4. **Error Handling** (explicit exceptions)
5. **Return Statement** (matches return type)

**Example:**

```python
def transform_customer_data(
    raw_data: Dict[str, Any],
    validation_rules: Optional[Dict[str, callable]] = None
) -> Customer:
    """
    Transform raw customer data into Customer model.
  
    Args:
        raw_data: Dictionary containing customer fields from source
        validation_rules: Optional custom validation functions per field
  
    Returns:
        Customer: Validated and transformed customer object
  
    Raises:
        ValueError: If required fields missing or validation fails
        TypeError: If field types don't match schema
  
    Example:
        >>> raw = {"id": "123", "name": "John", "email": "j@example.com"}
        >>> customer = transform_customer_data(raw)
        >>> assert customer.id == "123"
    """
    # Implementation here
    pass
```

---

## DOCSTRING TEMPLATES

### For Functions

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Single-line summary of what function does.
  
    More detailed explanation if needed. Describe the purpose,
    key behavior, and any important context.
  
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
  
    Returns:
        ReturnType: Description of return value
  
    Raises:
        ExceptionType: When and why this exception occurs
  
    Example:
        >>> result = function_name("value1", 42)
        >>> assert result.status == "success"
    """
```

### For Classes

```python
class ClassName:
    """
    Single-line summary of class purpose.
  
    Detailed description of what this class represents,
    its responsibilities, and how it fits into the system.
  
    Attributes:
        attribute1: Description of attribute
        attribute2: Description of attribute
  
    Example:
        >>> obj = ClassName(config)
        >>> obj.process()
    """
```

### For Modules

```python
"""
Module: module_name

Brief description of module purpose.

This module provides functionality for [X]. It contains:
- ClassA: Does X
- ClassB: Does Y
- function_z: Utility for Z

Usage:
    from module_name import ClassA
    obj = ClassA()
"""
```

---

## CORE LOGIC IMPLEMENTATION REQUIREMENTS

> **Layer 3 guidance logic standard:** The examples below show Developer-quality code as a *reference floor* — the minimum clarity to aim for. Layer 3 does not require full production robustness; it requires enough logic that a Developer reading the blueprint can understand exactly what the function is supposed to do and how it interacts with its dependencies.

### NOT Pseudocode

**Bad (Pseudocode):**

```python
def process_data(data):
    """Process the data."""
    # TODO: validate data
    # TODO: transform data
    # TODO: return result
    pass
```

**Good (Guidance Implementation):**

```python
def process_data(data: List[Dict[str, Any]]) -> List[Customer]:
    """
    Validate and transform raw data into Customer objects.
  
    Args:
        data: List of raw customer dictionaries
  
    Returns:
        List[Customer]: Validated customer objects
  
    Raises:
        ValueError: If any record fails validation
    """
    validated_customers = []
  
    for idx, record in enumerate(data):
        # Validate required fields
        required_fields = ['id', 'name', 'email']
        missing = [f for f in required_fields if f not in record]
        if missing:
            raise ValueError(f"Record {idx} missing fields: {missing}")
      
        # Transform to Customer
        customer = Customer(
            id=str(record['id']),
            name=record['name'].strip(),
            email=record['email'].lower(),
            created_at=datetime.now()
        )
      
        validated_customers.append(customer)
  
    return validated_customers
```

---

## INLINE COMMENTS FOR COMPLEX LOGIC

**When to add inline comments:**

- Non-obvious algorithms
- Business logic with specific rules
- Performance-critical optimizations
- Workarounds for library limitations
- Edge case handling

**Example:**

```python
def calculate_discount(price: float, customer_tier: str) -> float:
    """Calculate discounted price based on customer tier."""
  
    # Tier discounts: Bronze=5%, Silver=10%, Gold=15%, Platinum=20%
    tier_discounts = {
        'bronze': 0.05,
        'silver': 0.10,
        'gold': 0.15,
        'platinum': 0.20
    }
  
    discount_rate = tier_discounts.get(customer_tier.lower(), 0.0)
  
    # Apply discount but ensure minimum price of $1.00
    # (per business rule: no product can be free via discount)
    discounted = price * (1 - discount_rate)
    return max(discounted, 1.00)
```

---

## SAMPLE INPUT/OUTPUT REQUIREMENTS

**Every significant function needs example usage in docstring:**

```python
def merge_configs(base: Dict, override: Dict) -> Dict:
    """
    Merge two configuration dictionaries with override precedence.
  
    Args:
        base: Base configuration
        override: Override values (takes precedence on conflicts)
  
    Returns:
        Dict: Merged configuration
  
    Example:
        >>> base = {"timeout": 30, "retries": 3}
        >>> override = {"timeout": 60}
        >>> result = merge_configs(base, override)
        >>> assert result == {"timeout": 60, "retries": 3}
    """
    merged = base.copy()
    merged.update(override)
    return merged
```

---

## PHASE-BY-PHASE PROTOCOL

**For EACH Phase:**

1. **Load Context:** Read Layer 2 tasks for this phase
2. **Generate Skeleton:** Interfaces, types, signatures only — no logic yet
3. **Present Skeleton:** Get user approval
4. **Add Guidance Logic:** Add rudimentary logic, docstrings, and inline comments sufficient to direct the Developer — not production-complete implementation
5. **Present Blueprint:** Show complete structural blueprint with guidance logic
6. **Wait for Sign-off:** Get explicit approval before next phase

**Token Management:** One phase at a time maximizes context for deep implementation detail.

---

## QUALITY GATES

**Before presenting phase implementation:**

✅ **Type Safety:** All functions have type hints (params + return)
✅ **Documentation:** Every public function has complete docstring
✅ **Guidance Logic:** No bare `pass`/TODO stubs — each function communicates intended behavior through rudimentary logic (above pseudocode, sufficient to direct the Developer)
✅ **Error Handling:** Explicit exceptions defined and raised
✅ **Examples:** Key functions have usage examples in docstrings
✅ **Comments:** Complex logic has inline explanations
✅ **Consistency:** Naming conventions consistent across phase

**If any gate fails → refine before presenting**

---

## LANGUAGE-SPECIFIC STANDARDS

### Python

```python
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Model:
    """Use dataclasses for data models."""
    field1: str
    field2: int

def function_name(
    param: str,
    optional_param: Optional[int] = None
) -> Dict[str, Any]:
    """
    Function with type hints and optional parameters.
    """
    if optional_param is None:
        optional_param = 10
  
    return {"result": param, "value": optional_param}
```

### TypeScript

```typescript
interface Customer {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

/**
 * Transform raw customer data into Customer model.
 * 
 * @param rawData - Raw customer data from source
 * @returns Validated Customer object
 * @throws {ValidationError} If required fields missing
 * 
 * @example
 * ```typescript
 * const raw = { id: "123", name: "John", email: "j@example.com" };
 * const customer = transformCustomer(raw);
 * ```
 */
function transformCustomer(rawData: Record<string, any>): Customer {
  // Implementation
}
```

### SQL

```sql
-- Purpose: Retrieve active customers with recent orders
-- Parameters: @days_threshold - Number of days to look back
-- Returns: Customer records with order count

CREATE PROCEDURE GetActiveCustomers
    @days_threshold INT = 30
AS
BEGIN
    SELECT 
        c.customer_id,
        c.name,
        c.email,
        COUNT(o.order_id) as order_count
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_date >= DATEADD(DAY, -@days_threshold, GETDATE())
    GROUP BY c.customer_id, c.name, c.email
    HAVING COUNT(o.order_id) > 0
    ORDER BY order_count DESC;
END;
```

---

## COMMON PITFALLS

### ❌ AVOID: Skipping skeleton step

**Bad:** Writing full implementations immediately
**Good:** Generate skeleton → get approval → add guidance logic

### ❌ AVOID: Treating Layer 3 as production implementation

**Bad:** Writing fully production-complete, edge-case-hardened code in Layer 3
**Good:** Guidance blueprints that communicate intent — full production implementation is the Developer's role after Layer 5 Pure Signal brief is complete

### ❌ AVOID: Missing type hints

**Bad:** `def process(data):`
**Good:** `def process(data: List[Dict[str, Any]]) -> ProcessedData:`

### ❌ AVOID: Incomplete docstrings

**Bad:** `"""Process data."""`
**Good:** Full docstring with Args, Returns, Raises, Example

### ❌ AVOID: No error handling

**Bad:** Assumes all inputs valid
**Good:** Validates inputs, raises explicit exceptions

### ❌ AVOID: Magic numbers/strings

**Bad:** `if status == 3:`
**Good:** `if status == OrderStatus.COMPLETED:`

### ❌ AVOID: Unclear variable names

**Bad:** `def process(d, f, x):`
**Good:** `def process(data: List, filter_func: Callable, threshold: int):`

---

## IMPLEMENTATION PATTERNS

### Pattern: Repository

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class Repository(ABC):
    """Abstract base for data repositories."""
  
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Entity]:
        """Retrieve entity by ID."""
        pass
  
    @abstractmethod
    def get_all(self) -> List[Entity]:
        """Retrieve all entities."""
        pass
  
    @abstractmethod
    def create(self, entity: Entity) -> Entity:
        """Create new entity."""
        pass
  
    @abstractmethod
    def update(self, entity: Entity) -> Entity:
        """Update existing entity."""
        pass
  
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        pass
```

### Pattern: Service Layer

```python
class CustomerService:
    """Business logic for customer operations."""
  
    def __init__(self, repository: CustomerRepository):
        """Initialize with data repository."""
        self.repository = repository
  
    def register_customer(
        self,
        name: str,
        email: str
    ) -> Customer:
        """
        Register new customer with validation.
      
        Args:
            name: Customer full name
            email: Customer email address
      
        Returns:
            Customer: Newly created customer
      
        Raises:
            ValueError: If email already exists
            ValidationError: If inputs fail validation
        """
        # Validate email format
        if not self._is_valid_email(email):
            raise ValidationError(f"Invalid email: {email}")
      
        # Check for duplicates
        existing = self.repository.find_by_email(email)
        if existing:
            raise ValueError(f"Email already registered: {email}")
      
        # Create customer
        customer = Customer(
            id=self._generate_id(),
            name=name.strip(),
            email=email.lower(),
            created_at=datetime.now()
        )
      
        return self.repository.create(customer)
```

---

## EDGE CASE HANDLING

**Every implementation must consider:**

1. **Empty Inputs:** What if list is empty? String is ""?
2. **Null/None Values:** How to handle missing optional parameters?
3. **Type Mismatches:** What if wrong type passed?
4. **Boundary Conditions:** Min/max values, length limits
5. **Concurrency:** Race conditions, duplicate operations
6. **External Failures:** Database down, API timeout, network error

**Example:**

```python
def process_batch(items: List[Item]) -> ProcessResult:
    """Process batch of items with error resilience."""
  
    # Handle empty input
    if not items:
        return ProcessResult(processed=0, failed=0, errors=[])
  
    processed = []
    errors = []
  
    for item in items:
        try:
            # Validate item
            if not item or not item.id:
                errors.append({"item": item, "error": "Invalid item"})
                continue
          
            # Process
            result = self._process_single(item)
            processed.append(result)
          
        except Exception as e:
            # Isolate failures - one bad item doesn't stop batch
            errors.append({"item": item, "error": str(e)})
  
    return ProcessResult(
        processed=len(processed),
        failed=len(errors),
        errors=errors
    )
```

---

## SIGN-OFF PROTOCOL

**After completing ONE phase:**

1. **Present skeleton** → Get approval
2. **Present full implementation** with:
   - Number of functions/classes created
   - Key patterns used
   - Edge cases handled
3. **Ask:** "Does this technical blueprint for Phase N meet requirements? Any functions needing adjustment?"
4. **Wait for approval phrases:** "approved", "proceed", "looks good"
5. **Upon approval:** Move to next phase

**Do NOT proceed to Layer 4 until ALL phases have Layer 3 blueprints approved.**

> **Order of operations reminder:** Layer 3 blueprints → Layer 4 DRY audit → Layer 5 Pure Signal brief → Developer implementation. Handing to the Developer before Layer 5 is complete skips the compression and signal-extraction step that makes the handoff unambiguous.

---

## VERIFICATION CHECKLIST

**Per function:**

- [ ] Type hints on all parameters and return
- [ ] Complete docstring (summary, Args, Returns, Raises, Example)
- [ ] Actual logic (not pseudocode or TODO comments)
- [ ] Error handling with explicit exceptions
- [ ] Inline comments for complex sections
- [ ] Example usage in docstring

**Per phase:**

- [ ] All Layer 2 tasks have corresponding functions/classes
- [ ] Skeleton reviewed and approved before implementation
- [ ] Consistent naming conventions
- [ ] No code duplication (DRY violations will be caught in Layer 4)
- [ ] Edge cases considered and handled
