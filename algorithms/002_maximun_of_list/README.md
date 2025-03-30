# Maximum Value Finder - Algorithm Implementation

## Objective
Implement a manual maximum value search algorithm with production-grade error handling and type validation.

## Technical Overview

### Core Functionality
- Finds maximum value and its index in O(n) time complexity
- Handles both integers and floating-point numbers
- Returns tuple of (value, index)

### Key Features
- Type hints using `typing` module
- Comprehensive input validation:
  - Empty list detection (raises ValueError)
  - Type checking (raises TypeError)
- Multiple exception handling
- Example usage with test cases

## Implementation

```python
from typing import List, Tuple, Union

def max_list(input_list: List[Union[int, float]]) -> Tuple[Union[int, float], int]:
    """
    Finds the maximum value in a list and its index.

    Args:
        input_list: A list of integers or floats.
        
    Returns:
        Tuple containing (maximum_value, index_of_maximum)
        
    Raises:
        ValueError: If the list is empty.
        TypeError: If the list contains non-numeric values.
    """
    try:
        if not input_list:
            raise ValueError("The list cannot be empty.")

        if not all(isinstance(elt, (int, float)) for elt in input_list):
            raise TypeError("The list must contain only numbers (integers or floats).")

        # Find the maximum value and its index
        max_value, ind_max = input_list[0], 0
        for ind, val in enumerate(input_list):
            if val > max_value:
                max_value, ind_max = val, ind

        return max_value, ind_max

    except (ValueError, TypeError) as e:
        print(e)
    except Exception as e:
        print("An unexpected error occurred:", e)
```
## Test cases

```python
if __name__ == "__main__":
    test_cases = [
        [12, 87, -4, 0, 56, 33, -99, 102, 7, -23, 45, 89, 16, 38, -72],  # Normal case
        [],                                                              # Empty list
        [5, "hello", 3.14, None, 8],                                     # Mixed types
        [-3, -1, -2, -8],                                                # All negative
        [3.14, 1.59, 2.65],                                              # All floats
        [42]                                                           # Single element
    ]
    
    for case in test_cases:
        print(f"\nTesting list: {case}")
        result = max_list(case)
        if result is not None:
            print(f"Maximum value: {result[0]} at index {result[1]}")
        else:
            print("Invalid input (see error above)")
            
```