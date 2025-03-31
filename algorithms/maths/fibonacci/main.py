from typing import Dict, List

# Global cache for storing Fibonacci sequences
memory_fibonacci: Dict[int, List[int]] = {}

def fibonacci_seq(n: int) -> List[int]:
    """
    Generate the Fibonacci sequence up to the nth term.

    :param n: The number of terms in the Fibonacci sequence to generate.
    :return: A list containing the Fibonacci sequence up to the nth term.
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

# Test cases
mylist = [0, 5, 6, 12, "r", -4]

for number in mylist:
    try:
        print(fibonacci_seq(number))
    except Exception as e:
        print(f'Error: {e}')