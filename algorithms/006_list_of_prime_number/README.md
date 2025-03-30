# Prime Number Utilities - Algorithm Implementations

## Objective
Provide two prime number operations:
1. **Prime Check**: Verify if a number is prime (`is_prime`)
2. **Prime Generation**: List primes in a range (`list_prime`)

## Technical Overview

### Core Functionality
- Validates input types and ranges
- Implements trial division algorithm
- Handles edge cases (negative numbers, small primes)

### Function Comparison
| Feature          | is_prime               | list_prime             |
|------------------|------------------------|------------------------|
| Purpose          | Single number check    | Range generation       |
| Algorithm        | Trial division up to √n| Filter with is_prime() |
| Complexity       | O(√n)                  | O(n√n)                 |
| Error Handling   | Type/Value checks      | Additional range check |

## Implementations

### Prime Check (is_prime)
```python
def is_prime(n: int) -> bool:
    """
    Checks if a number is prime using trial division.
    
    Args:
        n: Integer to check
        
    Returns:
        True if prime, False otherwise
        
    Raises:
        TypeError: If input is not integer
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"The value {n} must be an integer.")

    if n < 2:
        return False

    n_sqrt = int(n ** 0.5)
    for i in range(2, n_sqrt + 1):
        if n % i == 0:
            return False
    return Trueù
```
### Prime Generation (list_prime)
```python 
def list_prime(p: int, q: int) -> List[int]:
    """
    Generates primes between p and q (inclusive).
    
    Args:
        p: Range start (inclusive)
        q: Range end (inclusive)
        
    Returns:
        List of primes in [p, q]
        
    Raises:
        TypeError: If inputs aren't integers
        ValueError: If p > q
    """
    if not isinstance(p, int) or not isinstance(q, int):
        raise TypeError("Both values must be integers.")

    if p > q:
        raise ValueError(f"The first value {p} must be smaller than or equal to the second {q}.")

    return [num for num in range(p, q + 1) if is_prime(num)]
```
### test cases

```python 
test_cases = [
    (10, 50),  # Normal range
    (2, 20),   # Small primes
    (-5, 15),  # Negative start
    (20, 10),  # Invalid range
    (5, "a"),  # Type error
    (17, 17),  # Single number
    (4, 4)     # Non-prime single
]

print("=== Prime Number Tests ===")
for p, q in test_cases:
    try:
        primes = list_prime(p, q)
        print(f"Primes between {p} and {q}: {primes}")
    except Exception as e:
        print(f"Error for ({p}, {q}): {e}")
```