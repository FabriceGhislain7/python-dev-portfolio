from typing import List, Dict, Union

def print_list(input_list: List[Union[dict, list, str, int]], indent: int = 0) -> None:
    """
    Print a nested list with indentation for nested levels.

    :param input_list: The list to print.
    :param indent: The number of spaces to indent for nested lists.
    :return: None
    """
    if not isinstance(input_list, list):
        raise TypeError("The parameter of the function shall be a non-empty list.")

    if not input_list:
        raise ValueError("The list cannot be empty.")

    tab = " " * indent
    for elt in input_list:
        if isinstance(elt, dict):
            print_dict(elt, indent + 2)  # Handle list of dictionaries correctly
        elif isinstance(elt, list):
            print_list(elt, indent + 2)
        else:
            print(tab + str(elt))

def print_dict(input_dict: Dict[str, Union[dict, list, str, int]], indent: int = 0) -> None:
    """
    Recursively prints a nested dictionary with proper indentation.

    :param input_dict: The dictionary to print.
    :param indent: The number of spaces to indent nested dictionaries.
    :return: None
    """
    if not isinstance(input_dict, dict):
        raise TypeError("The parameter of the function shall be a non-empty dictionary.")

    if not input_dict:
        raise ValueError("The dictionary cannot be empty.")

    tab = " " * indent
    for key, val in input_dict.items():
        print(f"{tab}{key}:")
        if isinstance(val, dict):
            print_dict(val, indent + 2)
        elif isinstance(val, list):
            print_list(val, indent + 2)
        else:
            print(f"{tab}  {val}")


# Example Data
library = {
    "Sci-Fi": {
        "books": [
            {"title": "Dune", "author": "Frank Herbert", "year": 1965, "tags": ["classic", "space"]},
            {"title": "Neuromancer", "author": "William Gibson", "year": 1984, "tags": ["cyberpunk", "AI"]}
        ]
    },
    "Fantasy": {
        "books": [
            {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "tags": ["classic", "adventure"]},
            {"title": "A Song of Ice and Fire", "author": "George R. R. Martin", "year": 1996,
             "tags": ["epic", "politics"]}
        ]
    },
    "Non-Fiction": {
        "books": [
            {"title": "Sapiens", "author": "Yuval Noah Harari", "year": 2011, "tags": ["history", "philosophy"]},
            {"title": "Educated", "author": "Tara Westover", "year": 2018, "tags": ["memoir", "education"]}
        ]
    }
}

# Run example
print_dict(library, indent=0)