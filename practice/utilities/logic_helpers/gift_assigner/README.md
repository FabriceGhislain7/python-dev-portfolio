# Random Gift Assigner (V 1.0)

## Description
This Python script assigns a random gift to each number from a given list. It ensures that every number is paired uniquely with a gift using a dictionary. The function also performs validation checks to avoid errors due to mismatched or empty lists.

## Features
- Randomly shuffles numbers and gifts for unique pairings.
- Ensures that both lists have the same length.
- Raises exceptions for empty lists or mismatched lengths.
- Uses type hints for better readability and maintainability.

## Installation
Ensure you have Python installed on your system (version 3.6+ recommended). No external dependencies are required.

## Usage
You can run the script as a standalone program or import the `dict_gift` function into another Python project.

### Function Definition
```python
import random
from typing import Dict, List

def dict_gift(numbers: List[int], gifts: List[str]) -> Dict[int, str]:
    """
    Associates each number in the list with a random gift.

    :param numbers: A list of unique numbers.
    :param gifts: A list of gifts.
    :return: A dictionary where each number is associated with a random gift.
    :raises ValueError: If the lists have different lengths or are empty.
    """
    if len(numbers) != len(gifts):
        raise ValueError("Both lists must have the same number of elements.")
    if not numbers or not gifts:
        raise ValueError("Both lists must contain at least one element.")

    random.shuffle(numbers)
    random.shuffle(gifts)

    return {numbers[i]: gifts[i] for i in range(len(numbers))}
```

### Example Usage
```python
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    gifts = ["Toy", "Book", "Mug", "Chocolate", "Plants", "Fountain Pen", "Watch", "Keychain", "Headphones", "Backpack"]
    
    try:
        result = dict_gift(numbers, gifts)
        for number, gift in result.items():
            print(f"{number}: {gift}")
    except ValueError as e:
        print(f"Error: {e}")
```

## Error Handling
- **Mismatched list lengths**: Raises a `ValueError` if numbers and gifts are not of equal length.
- **Empty lists**: Raises a `ValueError` if either list is empty.

## Contributing
Feel free to submit pull requests or suggest improvements!

## Contact
For any questions, reach out via GitHub Issues or email.


