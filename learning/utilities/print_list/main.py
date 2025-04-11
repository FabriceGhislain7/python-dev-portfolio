from typing import List

def print_list(input_list: List, indent: int = 0) -> None:
    """
    Print a nested list with indentation for nested levels.

    :param input_list: The list to print.
    :param indent: The number of spaces to indent for nested lists.
    :return: None
    """
    if not isinstance(input_list, List):
        raise TypeError("The parameter of the function shall be a non-empty list.")

    if not input_list:
        raise ValueError("The list cannot be empty.")

    tab = " " * indent
    for elt in input_list:
        if isinstance(elt, list):
            print_list(elt, indent=indent + 2)
        else:
            print(tab + str(elt))

# Test case
A = [6, 78, 20, 100, [-45, 400, 56, [7, 82, 824, 89], 109, 90, 89, 78], -90, 100]
print_list(A)