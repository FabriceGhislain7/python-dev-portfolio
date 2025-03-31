# Factorial Calculator - Algorithm Implementations

## Objective
Provide two implementations of factorial calculation:
1. **V1.0**: Iterative approach using a for loop
2. **V2.0**: Recursive approach with tail recursion optimization

## Technical Overview

### Core Functionality
- Calculates factorial of non-negative integers
- Input validation for type and range checking
- Consistent behavior for edge cases (0! and 1!)

### Version Comparison
| Feature               | V1.0 (Iterative)       | V2.0 (Recursive)       |
|-----------------------|------------------------|------------------------|
| Implementation        | For loop               | Tail recursion         |
| Stack Usage           | O(1)                  | O(n)*                 |
| Readability           | Straightforward        | Mathematic elegance    |
| Error Handling        | Identical              | Identical              |

*Python doesn't optimize tail recursion by default

## Implementations

### V1.0 - Iterative Implementation
```python
def factorial(n: int) -> int:
    """
    Calculates factorial using iterative approach.
    
    Args:
        n: Non-negative integer
        
    Returns:
        Factorial of n
        
    Raises:
        TypeError: If input is not integer
        ValueError: If input is negative
    """
    if not isinstance(n, int):
        raise TypeError(f"Input {n} must be integer")
    if n < 0:
        raise ValueError(f"Input {n} must be non-negative")
        
    if n in (0, 1):
        return 1
        
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

```
### V1.0 - Iterative Implementation

```python
def facto(n: int, acc: int = 1) -> int:
    """
    Calculates factorial using tail recursion.
    
    Args:
        n: Non-negative integer
        acc: Accumulator (internal use)
        
    Returns:
        Factorial of n
        
    Raises:
        TypeError: If input is not integer
        ValueError: If input is negative
    """

    if not isinstance(n, int):
        raise TypeError(f"Input {n} must be integer")
    if n < 0:
        raise ValueError(f"Input {n} must be non-negative")
        
    if n in (0, 1):
        return acc
    return facto(n-1, acc*n)
```
### Test cases
```python
test_values = [
    0,      # Edge case
    1,      # Edge case
    5,      # Normal case
    -3,     # Invalid case (negative)
    6.9,    # Invalid case (float)
    "r"     # Invalid case (string)
]

print("=== Factorial Calculator Tests ===")
for value in test_values:
    try:
        print(f"\nV1.0 Iterative: factorial({value})")
        print(f"Result: {factorial(value)}")
        
        print(f"\nV2.0 Recursive: facto({value})")
        print(f"Result: {facto(value)}")
    except Exception as e:
        print(f"Error: {e}")
```