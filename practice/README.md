
# Algorithms Toolkit

**A curated collection of Python algorithm implementations**  
*From fundamental building blocks to advanced problem-solving techniques*


## Directory Structure

```
utilities/
├── data_utils/
│   ├── print_dict/
│   └── print_list/
│
├── file_utils/
│   ├── files_manager/
│   └── json_contacts/          # (was rubrica_jason)
│
├── user_input/
│   └── age_prompt/
│
├── logic_helpers/
│   └── gift_assigner/
│
└── security/
    └── password_gen/
```

## Key Features

### Mathematical Algorithms
```python
# maths/fibonacci.py
def recursive_fib(n: int) -> int:
    """
    Compute nth Fibonacci number recursively
    :param n: Term index (0-based)
    :return: Fibonacci number
    :raises: ValueError for n < 0
    Time Complexity: O(2^n) [naive]
    Space Complexity: O(n) [call stack]
    """
    if n < 0:
        raise ValueError("Input must be non-negative")
    return n if n <= 1 else recursive_fib(n-1) + recursive_fib(n-2)
```

### Utility Functions
```python
# utilities/password_gen.py
def generate_secure_password(length=12) -> str:
    """
    Generates cryptographically secure passwords
    :param length: Desired password length (default: 12)
    :return: Secure password string
    Uses: secrets module (cryptographically strong)
    """
    import secrets
    import string
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))
```

## Usage Examples

1. **Running a single algorithm**:
```python
from maths.primes_list import generate_primes
primes = generate_primes(100)  # Generate primes up to 100
```

2. **Benchmarking**:
```bash
python -m timeit -s "from maths.factorial import recursive_fact" "recursive_fact(10)"
```

3. **Testing**:
```python
import pytest
from basics.min_of_list import find_min

def test_empty_list():
    with pytest.raises(ValueError):
        find_min([])
```

## Technical Specifications

| Category      | Key Algorithms       | Time Complexity   | Key Features                     |
|---------------|----------------------|-------------------|----------------------------------|
| Sorting       | sort_asc, sort_desc  | O(n log n)        | Pure Python implementations      |
| Math          | primes_list          | O(n log log n)    | Sieve algorithm                  |
| Security      | password_gen         | O(n)              | Cryptographically secure         |

## Development Guide

1. **Add new algorithm**:
```bash
mkdir maths/new_algorithm
touch maths/new_algorithm/{__init__.py,algorithm.py,test_algorithm.py,README.md}
```

2. **Testing standards**:
- 100% test coverage for core functions
- Edge case testing
- Performance benchmarks

3. **Style requirements**:
- PEP 8 compliance
- Type hints for all functions
- Google-style docstrings

---

*"Good algorithms are the soul of good programming."*
```
