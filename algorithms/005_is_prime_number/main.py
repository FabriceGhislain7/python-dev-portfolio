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

# Test cases
A = [8, 7, 356, 0, 99, -56, 8.0, 't', 2, 3, 17, 25]

for number in A:
    try:
        result = "Yes" if is_prime(number) else "No"
        print(f"{number} is a prime number? {result}")
    except Exception as e:
        print(f"Error: {e}")
    print()
