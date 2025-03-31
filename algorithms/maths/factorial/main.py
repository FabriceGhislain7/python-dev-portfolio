# First Method
def factorial(n: int) -> int:
    """
    This function calculates the factorial of an integer number "n" and returns it.
    :param n: The integer number for which the factorial is calculated.
    :return: The factorial of the input number.
    """
    if not isinstance(n, int):
        raise TypeError(f"The input value {n} must be an integer.")
    if n < 0:
        raise ValueError(f"The input value {n} must be a non-negative integer.")

    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(1, n+1):
        result *= i
    return result

# Second Method : Recursive function with an optional parameter acc=1
def facto(n: int, acc:int =1) -> int:
    """
    This function calculates the factorial of an integer number "n" and returns it.
    :param n: The integer number for which the factorial is calculated.
    :return: The factorial of the input number.
    :param acc: The accumulator that stores intermediate results (default is 1).
                This parameter is used internally for tail recursion optimization.
    """

    if not isinstance(n, int, ):
        raise TypeError(f"The input value {n} must be an integer.")
    if n < 0:
        raise ValueError(f"The input value {n} must be a non-negative integer.")

    return 1 if n == 0 or n == 1 else facto(n-1, acc*n)



# Example usage
numbers = [6.9, 5, -78, "r"]
for num in numbers:
    try:
        # To test both of method, you can substitute the function "factorial()" by "facto()"
        print(f"The factorial of {num} is {factorial(num)}")
    except Exception as e:
        print(f"Error: {e}")
    print()
