import random
import string

def generate_password(
        length: int,
        has_lowercase: bool = True,
        has_uppercase: bool = True,
        has_number: bool = True,
        has_special_chars: bool = True) -> str:
    """
    Generates a random password based on the specified criteria.

    :param length: The length of the password (must be at least 8).
    :param has_lowercase: Include lowercase letters if True.
    :param has_uppercase: Include uppercase letters if True.
    :param has_number: Include numbers if True.
    :param has_special_chars: Include special characters if True.
    :return: A randomly generated password.
    :raises ValueError: If the length is less than 8 or no character types are selected.
    """
    if length < 8 or not isinstance(length, int):
        raise ValueError("The password must have at least 8 characters.")

    if not any([has_lowercase, has_uppercase, has_number, has_special_chars]):
        raise ValueError("At least one character type must be selected.")

    # Define character sets based on user preferences
    lower = string.ascii_lowercase if has_lowercase else ""
    upper = string.ascii_uppercase if has_uppercase else ""
    numbers = string.digits if has_number else ""
    special_chars = string.punctuation if has_special_chars else ""

    # Combine all allowed characters
    all_chars = lower + upper + numbers + special_chars

    # Ensure at least one character from each selected type is included
    password = []
    if has_lowercase:
        password.append(random.choice(lower))
    if has_uppercase:
        password.append(random.choice(upper))
    if has_number:
        password.append(random.choice(numbers))
    if has_special_chars:
        password.append(random.choice(special_chars))

    while len(password) < length:
        password.append(random.choice(all_chars))

    random.shuffle(password)

    return "".join(password)

# Example usage
if __name__ == "__main__":
    # Test cases
    try:
        print(generate_password(12))
        print(generate_password(10, has_special_chars=False))
        print(generate_password(8, has_lowercase=False, has_uppercase=False))
        print(generate_password(5))
    except ValueError as e:
        print(e)