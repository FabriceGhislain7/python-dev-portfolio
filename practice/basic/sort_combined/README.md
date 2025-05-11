# List Utilities - Min, Max, and Sorting Functions

## Objective
Provide three core list operations:
1. Find minimum value and index (`min_list`)
2. Find maximum value and index (`max_list`)
3. Sort list in ascending/descending order (`sorted_list`)

## Technical Overview

### Core Functionality
- `min_list`: Finds minimum value and index in O(n) time
- `max_list`: Finds maximum value and index in O(n) time
- `sorted_list`: Implements selection sort using O(n²) time complexity

### Key Features
| Feature               | min_list               | max_list               | sorted_list            |
|-----------------------|------------------------|------------------------|------------------------|
| Input Validation      | Yes                    | Yes                    | Yes                    |
| Error Handling        | Detailed               | Detailed               | Detailed               |
| Return Type           | Tuple (value, index)   | Tuple (value, index)   | New sorted list        |
| Order Control         | N/A                    | N/A                    | Ascending/Descending   |

## Implementations

### min_list Implementation
```python
from typing import List, Tuple, Union

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
```
### max_list Implementation
```python
from typing import List, Tuple, Union

def max_list(input_list: List[Union[int, float]]) -> Tuple[Union[int, float], int]:
    """
    Finds the maximum value in a list and its index.

    :param input_list: A list of integers or floats.
    :return: A tuple containing the maximum value and its index.
    :raises ValueError: If the list is empty.
    :raises TypeError: If the list contains non-numeric values.
    """
    if not input_list:
        raise ValueError("ValueError: The list cannot be empty.")

    if not all(isinstance(elt, (int, float)) for elt in input_list):
        raise TypeError("TypeError: The list must contain only numbers (integers or floats).")

    max_value, ind_max = input_list[0], 0
    for ind, val in enumerate(input_list):
        if val > max_value:
            max_value, ind_max = val, ind

    return max_value, ind_max

```
### sorted_list Implementation
```python 
from typing import List, Tuple, Union

def sorted_list(input_list: List[Union[int, float]], sort_order: bool) -> List[Union[int, float]]:
    """
    Sorts a list of integers or floats in ascending or descending order.

    :param input_list: A list of integers or floats.
    :param sort_order: If True, sorts in ascending order. If False, sorts in descending order.
    :return: A new list sorted in the specified order.
    :raises ValueError: If the list is empty or contains non-numeric values.
    :example:
    #    >>> sorted_list([3, 1, 4, 1, 5], True)
        [1, 1, 3, 4, 5]
    #    >>> sorted_list([3, 1, 4, 1, 5], False)
        [5, 4, 3, 1, 1]
    """
    if not input_list:
        raise ValueError("The input list can't be empty.")

    if not all(isinstance(x, (int, float)) for x in input_list):
        raise ValueError("The list shall contain only integers or float numbers.")

    order_list = []
    working_list = input_list.copy()

    while len(working_list) != 0:
        if sort_order:
            val, ind = min_list(working_list)
        else:
            val, ind = max_list(working_list)
        order_list.append(val)
        working_list.pop(ind)

    return order_list

```
### Test cases
```python
test_lists = [
    [12, 87, -4, 0, 56, 33, -99, 102, 7, -23, 45, 89, 16, 38, -72],  # Normal case
    [],                                                                 # Empty list
    [5, "hello", 3.14, None, 8],                                       # Mixed types
    [3.14, -2.5, 10, 0, 7.7]                                           # Floats
]

print("=== List Utilities Tests ===")
for lst in test_lists:
    try:
        print(f"\nOriginal: {lst}")
        print(f"Min value: {min_list(lst)}")
        print(f"Max value: {max_list(lst)}")
        print(f"Sorted (ascending): {sorted_list(lst, True)}")
        print(f"Sorted (descending): {sorted_list(lst, False)}")
    except Exception as e:
        print(f"Error: {e}")
```



