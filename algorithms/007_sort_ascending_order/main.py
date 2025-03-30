from typing import Union, List, Tuple

def min_list(input_list: List[Union[int, float]]) -> Tuple[Union[int, float], int]:
    """
    Finds the minimum value in a list and its index.

    :param input_list: A list of integers or floats.
    :return: A tuple containing the minimum value and its index.
    :raises ValueError: If the list is empty.
    :raises TypeError: If the list contains non-numeric values.
    """
    if not input_list:
        raise ValueError("ValueError: The list cannot be empty.")

    if not all(isinstance(elt, (int, float)) for elt in input_list):
        raise TypeError("TypeError: The list must contain only numbers (integers or floats).")

    min_value, ind_min = input_list[0], 0
    for ind, val in enumerate(input_list):
        if val < min_value:
            min_value, ind_min = val, ind

    return min_value, ind_min

def sorted_list(input_list: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Sorts a list of integers or floats in ascending order.

    :param input_list: A list of integers or floats.
    :return: A new list sorted in ascending order.
    :raises ValueError: If the list is empty or contains non-numeric values.
    """
    if not input_list:
        raise ValueError("The input list can't be empty.")

    if not all(isinstance(x, (int, float)) for x in input_list):
        raise ValueError("The list shall contain only integers or float numbers.")

    order_list = []
    test_list = input_list.copy()

    while len(test_list) != 0:
        val, ind = min_list(test_list)
        order_list.append(val)
        test_list.pop(ind)

    return order_list

# Example usage
if __name__ == "__main__":
    # Test cases
    A = [12, 87, -4, 0, 56, 33, -99, 102, 7, -23, 45, 89, 16, 38, -72]
    B = []
    C = [5, "hello", 3.14, None, 8]
    D = [3.14, -2.5, 10, 0, 7.7]

    lists = [A, B, C, D]
    for single_list in lists:
        print(f"For the list {single_list}:")
        try:
            result = sorted_list(single_list)
            print(f"Sorted list: {result}")
        except (ValueError,TypeError) as e:
            print(e)
        except Exception as e:
            print("An unknown error occurred:", e)
        print()