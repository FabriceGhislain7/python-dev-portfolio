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

    # Shuffle both lists to ensure random association
    random.shuffle(numbers)
    random.shuffle(gifts)

    # Create a dictionary to associate numbers with gifts
    game_gifts: Dict[int, str] = {}
    for i in range(len(numbers)):
        game_gifts[numbers[i]] = gifts[i]

    return game_gifts

# Example usage
if __name__ == "__main__":
    # Test data
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    gifts = [
        "Toy", "Book", "Mug", "Chocolate", "Plants", "Fountain Pen",
        "Watch", "Keychain", "Headphones", "Backpack", "Perfume", "T-Shirt",
        "Puzzle", "Drawing Set", "Thermal Bag", "Planner", "Scented Candles",
        "Board Game", "Pajamas", "Bottle of Wine"
    ]

    # Generate the dictionary
    try:
        result = dict_gift(numbers, gifts)

        # Print the result with indentation
        for ind, (number, gift) in enumerate(result.items()):
            print(f"{' ' * ind}{number}: {gift}")
    except ValueError as e:
        print(e)