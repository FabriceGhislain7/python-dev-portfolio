# Prime Number Checker - Algorithm Implementation

## Objective
Implement an efficient primality test algorithm that determines whether a given integer is a prime number.

## Technical Overview

### Core Functionality
- Determines if a number is prime using trial division up to √n
- Handles edge cases (numbers < 2)
- Includes type validation
- Returns boolean result

### Key Features
- Optimized O(√n) time complexity
- Comprehensive input validation
- Clear error messaging
- Simple boolean return interface

## Implementation

```python
def is_prime(n: int) -> bool:
    """
    Checks if a number is prime using optimized trial division.
    
    Args:
        n: Integer to check for primality
        
    Returns:
        True if prime, False otherwise
        
    Raises:
        TypeError: If input is not integer
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"Input {n} must be integer (not boolean)")

    if n < 2:
        return False

    n_sqrt = int(n ** 0.5) + 1
    for i in range(2, n_sqrt):
        if n % i == 0:
            return False
    return True
```
### Test cases

```python 
test_values = [
    2,      # Smallest prime
    3,      # Prime
    17,     # Prime
    25,     # Composite (5²)
    8,      # Composite
    7,      # Prime
    356,    # Composite
    0,      # Edge case
    -56,    # Negative
    8.0,    # Invalid (float)
    't',    # Invalid (string)
    True    # Invalid (boolean)
]

print("=== Prime Number Checker Tests ===")
for value in test_values:
    try:
        result = "Prime" if is_prime(value) else "Not prime"
        print(f"{value:>4} → {result}")
    except Exception as e:
        print(f"{value:>4} → Error: {e}")
```