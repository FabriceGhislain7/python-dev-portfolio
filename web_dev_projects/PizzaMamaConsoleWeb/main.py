import requests
import json

url = "https://fabricedeveloper.pythonanywhere.com/api/GetPizzas"

try:
    response = requests.get(url)
    response.raise_for_status()  # raises an error if the status code is not 200
    pizzas = response.json()     # simpler than using json.loads(response.text)

    print(len(pizzas))
    for pizzaModel in pizzas:
        pizza = pizzaModel['fields']
        print(f"{pizza['name']}: {pizza['price']} €")

except requests.exceptions.RequestException as e:
    print("HTTP request error:", e)

except json.JSONDecodeError:
    print("Error decoding the JSON response.")
