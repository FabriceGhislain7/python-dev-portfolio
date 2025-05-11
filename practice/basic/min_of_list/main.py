from typing import List, Tuple, Union

def find_min_value(input_list: List[Union[int, float]]) -> Tuple[Union[int, float], int]:
    """
    Finds the minimum value in a list and its index (implemented from scratch).
    
    Args:
        input_list: List of numbers (integers and/or floats)
        
    Returns:
        Tuple containing (minimum_value, index_of_minimum)
        
    Raises:
        ValueError: If input list is empty
        TypeError: If list contains non-numeric values
    """
    # Check for empty list
    if len(input_list) == 0:
        raise ValueError("Input list cannot be empty")
    
    # Initialize variables to track minimum
    min_value = input_list[0]
    min_index = 0
    
    # Iterate through the list
    for current_index, current_value in enumerate(input_list):
        # Type checking
        if not isinstance(current_value, (int, float)):
            raise TypeError("List must contain only numeric values")
        
        # Update minimum if current value is smaller
        if current_value < min_value:
            min_value = current_value
            min_index = current_index
    
    return (min_value, min_index)

# Test cases                  # I added some wrong cases to capture the errors.
if __name__ == "__main__":      
    test_cases = [
        [5, 2, 8, 1, 4],      # Normal case
        [-3, -10, -2, -8],    # All negative numbers
        [1.5, 2.3, 0.7],      # Floating point numbers
        [42],                 # Single element
        [],                   # Empty list (should raise error)
        [1, "two", 3],        # Mixed types (should raise error)
    ]
    
    for case in test_cases:
        print(f"\nTesting list: {case}")
        try:
            min_val, min_idx = find_min_value(case)
            print(f"Minimum value: {min_val} at index {min_idx}")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")