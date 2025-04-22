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