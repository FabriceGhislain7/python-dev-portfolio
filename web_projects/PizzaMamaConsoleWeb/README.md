# 🍕 Pizzamama API Client

This is a simple Python client to interact with the **Pizzamama** REST API hosted on [PythonAnywhere](https://fabricedeveloper.pythonanywhere.com/api/GetPizzas).  
It allows users to fetch and display a list of pizzas along with their prices.

---

## 🔗 API Endpoint

```
GET https://fabricedeveloper.pythonanywhere.com/api/GetPizzas
```

Returns a list of pizzas in JSON format.

---

## ✅ Requirements

- Python 3.6+  [Python **3.10.3** (exact version used in this project)]
- `requests` library (`pip install requests`)

---

## Version 1: Basic Script

A simple script using the `requests` module to fetch and print the list of pizzas.

```python
import requests
import json

url = "https://fabricedeveloper.pythonanywhere.com/api/GetPizzas"

try:
    response = requests.get(url)
    response.raise_for_status()  # raises an error if the status code is not 200
    pizzas = response.json()

    print(len(pizzas))
    for pizzaModel in pizzas:
        pizza = pizzaModel['fields']
        print(f"{pizza['name']}: {pizza['price']} €")

except requests.exceptions.RequestException as e:
    print("HTTP request error:", e)
except json.JSONDecodeError:
    print("Error decoding the JSON response.")
```

---

## Version 2: Class-Based Client

A reusable and more structured approach using a Python class.

```python
import requests
import json

class PizzaAPI:
    BASE_URL = "https://fabricedeveloper.pythonanywhere.com/api"

    @classmethod
    def get_pizzas(cls):
        try:
            response = requests.get(f"{cls.BASE_URL}/GetPizzas", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request error: {e}")
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
        return None

if __name__ == "__main__":
    pizzas = PizzaAPI.get_pizzas()
    if pizzas:
        print(f"\nFound {len(pizzas)} pizza(s):\n")
        for i, pizzaModel in enumerate(pizzas, 1):
            pizza = pizzaModel.get('fields', {})
            name = pizza.get('name', 'Unknown')
            price = pizza.get('price', '?')
            print(f"{i}. {name} - {price} €")
    else:
        print("No pizzas found or an error occurred.")
```

---

## Upcoming: Rich-Powered Custom Terminal Version

We are working on a **customized version of the API client** using the [`rich`](http://rich.readthedocs.io/en/stable/) library — a Python package for beautiful terminal formatting. It will include:

- Colorized pizza lists 🍕
- Fancy tables with borders and highlights
- Loading spinners and progress bars while fetching data
- Improved error display with styling

✨ Stay tuned for **Version 3**!

> Install `rich` if you want to prepare for it:
```bash
pip install rich
```

---

## License

Free to use for educational or hobby projects 

---

## Author

Made by [@fabricedeveloper](https://github.com/fabricedeveloper) 
