from typing import List


def is_prime(n: int) -> bool:
    """
    Checks if a number is prime.
    :param n: The number to check
    :return: True if n is prime, otherwise False
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"The value {n} must be an integer.")

    if n < 2:
        return False

    n_sqrt = int(n ** 0.5)
    for i in range(2, n_sqrt + 1):
        if n % i == 0:
            return False
    return True


def list_prime(p: int, q: int) -> List[int]:
    """
    Returns a list of prime numbers between p and q (inclusive).
    :param p: The start of the range (inclusive)
    :param q: The end of the range (inclusive)
    :return: List of prime numbers in the range [p, q]
    """
    if not isinstance(p, int) or not isinstance(q, int):
        raise TypeError("Both values must be integers.")

    if p > q:
        raise ValueError(f"The first value {p} must be smaller than or equal to the second {q}.")

    return [num for num in range(p, q + 1) if is_prime(num)]


# Test cases for list_prime function
test_cases = [(10, 50),(2, 20),(-5, 15),
              (20, 10),(5, "a"),(8.5, 20),
              ("b", 15),(17, 17),(4, 4),]
for p, q in test_cases:
    try:
        result = list_prime(p, q)
        print(f"Prime numbers between {p} and {q}: {result}")
    except Exception as e:
        print(f"Error for inputs ({p}, {q}): {e}")
    print()

