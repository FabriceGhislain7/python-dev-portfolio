from typing import List, Tuple, Union

def max_list(input_list: List[Union[int, float]]) -> Tuple[Union[int, float], int]:
    """
    Finds the maximum value in a list and its index.

    :param input_list: A list of integers or floats.
    :return: A tuple containing the maximum value and its index.
    :raises ValueError: If the list is empty.
    :raises TypeError: If the list contains non-numeric values.
    """
    try:
        if not input_list:
            raise ValueError("The list cannot be empty.")

        if not all(isinstance(elt, (int, float)) for elt in input_list):
            raise TypeError("The list must contain only numbers (integers or floats).")

        # Find the maximum value and its index using enumerate()
        max_value, ind_max = input_list[0], 0
        for ind, val in enumerate(input_list):
            if val > max_value:
                max_value, ind_max = val, ind

        return max_value, ind_max

    except (ValueError, TypeError) as e:
        print(e)
    except Exception as e:
        print("An unexpected error occurred:", e)


# Example usage
A = [12, 87, -4, 0, 56, 33, -99, 102, 7, -23, 45, 89, 16, 38, -72]
B = []  #
C = [5, "hello", 3.14, None, 8]

lists = [A, B, C]
for single_list in lists:
    print(f"For the list {single_list}:")
    result = max_list(single_list)
    if result is not None:
        print(f"Maximum value and index are: {result}")
    else:
        print("No valid result.")
    print()
