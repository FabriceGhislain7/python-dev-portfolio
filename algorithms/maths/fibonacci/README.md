# Fibonacci Sequence Generator

## Description
This Python script generates the Fibonacci sequence up to a specified term. It utilizes a global cache to store previously computed sequences, improving efficiency when generating sequences for the same input multiple times.

## Features
- Computes the Fibonacci sequence up to a given number of terms.
- Implements caching to store and retrieve previously computed sequences.
- Performs validation checks for input types and values.
- Manages cache size to prevent excessive memory usage.

## Installation
Ensure you have Python installed on your system (version 3.6+ recommended). No external dependencies are required.

## Usage
You can run the script as a standalone program or import the `fibonacci_seq` function into another Python project.

### Function Definition
```python
from typing import Dict, List

# Global cache for storing Fibonacci sequences
memory_fibonacci: Dict[int, List[int]] = {}

def fibonacci_seq(n: int) -> List[int]:
    """
    Generate the Fibonacci sequence up to the nth term.

    :param n: The number of terms in the Fibonacci sequence to generate.
    :return: A list containing the Fibonacci sequence up to the nth term.
    :raises TypeError: If the input is not an integer.
    :raises ValueError: If the input is a negative integer.
    """
    if not isinstance(n, int):
        raise TypeError("The input must be a positive integer.")
    if n < 0:
        raise ValueError("The input must be a non-negative integer.")

    if n in memory_fibonacci:
        return memory_fibonacci[n]

    if n == 0:
        sequence = [0]
    elif n == 1:
        sequence = [0, 1]
    else:
        sequence = [0, 1]
        for i in range(2, n + 1):
            sequence.append(sequence[i - 2] + sequence[i - 1])
    memory_fibonacci[n] = sequence

    # Manage cache size (optional)
    if len(memory_fibonacci) > 100:
        memory_fibonacci.pop(next(iter(memory_fibonacci)))

    return sequence
```

### Example Usage
```python
# Test cases
mylist = [0, 5, 6, 12, "r", -4]

for number in mylist:
    try:
        print(fibonacci_seq(number))
    except Exception as e:
        print(f'Error: {e}')
```

## Error Handling
- **Non-integer input**: Raises a `TypeError` if the input is not an integer.
- **Negative integer input**: Raises a `ValueError` if the input is negative.

## Contributing
Feel free to submit pull requests or suggest improvements!

