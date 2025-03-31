# Age Calculator

## Description
This Python script calculates a person's age in years, months, and days based on their date of birth.

## Features
- Computes the exact age using years, months, and days.
- Handles incorrect inputs with proper error messages.
- Uses `dateutil.relativedelta` for accurate date calculations.

## Installation
Ensure you have Python installed on your system (version 3.6+ recommended). You also need the `dateutil` package, which can be installed using:

```sh
pip install python-dateutil
```

## Usage
You can run the script as a standalone program or import the `get_age` function into another Python project.

### Function Definition
```python
from typing import Tuple
import datetime
from dateutil.relativedelta import relativedelta

def get_age(day: str, month: str, year: str) -> Tuple[int, int, int]:
    """
    Calculate a person's age in years, months, and days from their date of birth.

    :param day: Day of birth (as a string, e.g., "04")
    :param month: Month of birth (as a string, e.g., "01")
    :param year: Year of birth (as a string, e.g., "1988")
    :return: A tuple (years, months, days) representing the age
    """
    try:
        # Convert strings to integers
        day_int = int(day)
        month_int = int(month)
        year_int = int(year)

        # Create a date object
        birthday = datetime.date(year_int, month_int, day_int)
    except ValueError as e:
        raise ValueError(f"Invalid date of birth: {e}")

    today = datetime.date.today()

    # Calculate age using relativedelta
    delta = relativedelta(today, birthday)
    return delta.years, delta.months, delta.days
```

### Example Usage
```python
age = get_age("03", "01", "1989")
print(f"Age: {age[0]} years, {age[1]} months, {age[2]} days")
```

## Error Handling
- **Invalid date format**: Raises a `ValueError` if the date cannot be parsed.
- **Non-numeric input**: Raises a `ValueError` if non-numeric values are passed.

## Contributing
Feel free to submit pull requests or suggest improvements!
