# Nested List Printer

## Description
This Python script prints a nested list with indentation to visually represent nested levels. It ensures proper formatting by increasing indentation for each deeper level.

## Features
- Handles nested lists of arbitrary depth.
- Properly indents nested elements for readability.
- Performs validation checks for input types and non-empty lists.

## Installation
Ensure you have Python installed on your system (version 3.6+ recommended). No external dependencies are required.

## Usage
You can run the script as a standalone program or import the `print_list` function into another Python project.

### Function Definition
```python
from typing import List

def print_list(input_list: List, indent: int = 0) -> None:
    """
    Print a nested list with indentation for nested levels.

    :param input_list: The list to print.
    :param indent: The number of spaces to indent for nested lists.
    :return: None
    :raises TypeError: If the input is not a list.
    :raises ValueError: If the list is empty.
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
```

### Example Usage
```python
# Test case
A = [6, 78, 20, 100, [-45, 400, 56, [7, 82, 824, 89], 109, 90, 89, 78], -90, 100]
print_list(A)
```

## Error Handling
- **Non-list input**: Raises a `TypeError` if the input is not a list.
- **Empty list input**: Raises a `ValueError` if the list is empty.

## Contributing
Feel free to submit pull requests or suggest improvements!


