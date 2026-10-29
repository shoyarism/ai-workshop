---
name: adversarial-debugging
description: Rigorously debug code by systematically challenging assumptions, hunting tail risks, and stress-testing edge cases before trusting any implementation.
tags:
  - debugging
  - adversarial
  - testing
  - robustness
category: dev-house
version: 1.0.0
---

# adversarial-debugging

A systematic approach to debugging that treats every assumption as a potential bug, every happy path as a liability, and every "working" solution as a latent time bomb.

## When to Apply

- Code passes tests but behavior is "magical" or unexplainable
- Production issues that don't reproduce in dev
- AI-generated code with suspiciously clean patterns
- Any code that makes you say "this should work" (it usually doesn't)

## The Adversarial Debug Protocol

### Phase 1: Inversion (What's Wrong with Our Assumptions?)

1. **Question Everything**: For each function, ask "What if this returns the *opposite* of what we expect?"
2. **Input Inversion**: 
   - Replace expected inputs with `null`, `""`, `0`, `[]`, `{}`
   - Test type coercion: `"0"`, `"false"`, `null` in boolean contexts
   - Feed adversarial inputs: SQL injection strings to non-SQL fns

3. **State Inversion**:
   ```python
   # Before: assume initialized state
   obj = MyClass()
   print(obj.value)  # What if .value doesn't exist?
   
   # After: test uninitialized/corrupted state
   obj._internal_state = None
   obj.cache = {}
   del obj.required_attr
   ```

### Phase 2: Tail Risk Hunting

Find the failure modes that "can't possibly happen":

```python
# Systematic failure injection points
FAILURE_MODES = [
    "Network timeout before header",
    "Connection reset mid-read",
    "File truncated at 1 byte",
    "Permissions changed mid-operation",
    "Clock jumps backward",
    "Memory exhausted",
    "Locale changes during processing",
    "Unicode normalize mismatch",
]

def stress_test(func, inputs, failure_modes=FAILURE_MODES):
    """Inject every conceivable failure mode."""
    for mode in failure_modes:
        with mock_failure_mode(mode):
            try:
                result = func(**inputs)
                log_failure(mode, result)  # Should raise, didn't!
            except ExpectedException as e:
                pass  # Good, this failure is handled
            except Exception as e:
                log_unexpected_failure(mode, e)
```

### Phase 3: Boundary Condition Smashing

Test at the edges:

```python
def test_boundaries(func):
    # Integer boundaries
    for n in [0, -1, 1, 2**31-1, -2**31, None]:
        test_with_input(n)
    
    # String boundaries
    for s in ["", " ", "\0", "\n", "\r\n", "a" * 10**6, "🚀"]:
        test_with_input(s)
    
    # Collection boundaries
    for items in [[], [None], [0], [{}], [[]] * 1000]:
        test_with_input(items)
```

### Phase 4: Chaos Monkey for Deterministic Failures

```python
class ChaosMonkey:
    """Inject deterministic failures for reproducible debugging."""
    
    def __init__(self):
        self.failures = {
            "network": [("timeout", 5), ("corrupt", 3)],
            "disk": [("full", 1), ("latency", 1000)],
            "time": [("jump", -3600), ("freeze", 10)],
        }
        self.call_count = defaultdict(int)
    
    def maybe_fail(self, resource, op):
        """50% chance to fail on Nth call for reproducibility."""
        if resource not in self.failures:
            return
        
        fails = self.failures[resource]
        for failure, count in fails:
            self.call_count[(resource, op)] += 1
            if self.call_count[(resource, op)] % count == 0:
                raise deterministic_failure(failure, resource, op)
```

## Anti-Pattern Catalog

| Pattern | How to Debug |
|---------|--------------|
| `if x:` without `is not None` | Test `x = 0`, `x = ""`, `x = []`, `x = False` |
| `except Exception: pass` | Always log, re-raise with context |
| `return result or default` | What if `result` is falsy but valid? |
| `@cache` without TTL | Cache poisoning, memory leaks |
| `type(x) == Type` | Use `isinstance(x, Type)` |
| `json.loads(json.dumps(x))` | Data mutation, precision loss |

## CLI Tool Integration

```bash
# Initialize adversarial debug session
python scripts/debug.py start <function_path> --mode full-spectrum

# Run boundary smash test
python scripts/debug.py boundary <function_path> --inputs "0,-1,1,1e308"

# Inject chaos
python scripts/debug.py chaos <function_path> --fail "network:timeout,disk:full"
```

## Example Debug Session

Before debugging (naive approach):
```python
def process_payment(user_id, amount):
    user = get_user(user_id)
    charge = create_charge(user.card, amount)
    return {"status": "ok", "charge_id": charge.id}
```

After adversarial debugging:
```python
def process_payment(user_id: int, amount: Decimal) -> dict:
    """
    Process payment with adversarial hardening.
    
    Returns: Dict with status and charge_id or error_code
    Raises: PaymentError with descriptive message
    """
    # Pre-condition validation (FEL-08 defense)
    if not isinstance(user_id, int) or user_id <= 0:
        raise PaymentError("INVALID_USER_ID")
    
    if not isinstance(amount, Decimal) or amount <= 0:
        raise PaymentError("INVALID_AMOUNT")
    
    # Get user with timeout and circuit breaker
    try:
        with timeout(5), circuit_breaker():
            user = get_user(user_id)
    except UserNotFoundError:
        raise PaymentError("USER_NOT_FOUND")
    except TimeoutError:
        raise PaymentError("USER_LOOKUP_TIMEOUT")
    
    # Validate card exists
    if not user.has_valid_card():
        raise PaymentError("CARD_REQUIRED")
    
    # Process charge with idempotency
    idempotency_key = f"charge-{user_id}-{amount}-{uuid4()}"
    try:
        charge = create_charge(
            card_token=user.card_token,
            amount_cents=int(amount * 100),
            idempotency_key=idempotency_key
        )
    except InsufficientFundsError:
        raise PaymentError("INSUFFICIENT_FUNDS")
    except CardExpiredError:
        raise PaymentError("CARD_EXPIRED")
    except GatewayError as e:
        log_error("GATEWAY_ERROR", e)
        raise PaymentError("PROCESSING_FAILED")
    
    # Never return raw exception
    return {
        "status": "ok" if charge.status == "succeeded" else "pending",
        "charge_id": charge.id,
        "amount": charge.amount,
        "currency": charge.currency
    }
```

## Related Skills

- [[systematic-debugging]] - Standard debugging patterns
- [[debug-house/potential-things-that-can-go-wrong|SLOWS]] - Common failure catalog  
- [[dev-house/tdd|Test-Driven Discipline]] - Testing as debugging
- [[security-house/strix-pentest|Pentest Red Teaming]] - Adversarial security approach

## References

- [Chaos Engineering Principles](https://principlesofchaosengineering.org/)
- [Property-Based Testing](https://hypothesis.works/)
- [The Art of Debugging](https://www.amazon.com/Art-Debugging-Programmers-Systems-Analysts/dp/020162641X)