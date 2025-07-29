# 🍕 PizzaMama - Digital Menu System for Pizzerias

**PizzaMama** is a Django-based application that allows the management of a pizza menu through an admin interface and a simple API. The project is designed to evolve into a full-featured online ordering platform.

> ⚠️ **Note**: while the code and models are written in **English**, the menu shown on the frontend is displayed in **French**.

---
## View PizzaMama Interface Screenshot
<details>
<summary>📸 Click to view screenshot</summary>

![PizzaMama Interface](pizzamama/menu/static/menu/images/pizzamama.jpg)

</details>

---

## Features

- ☑️ Display of the pizza menu  
- ☑️ Admin interface using Django  
- ☑️ Tag system for vegetarian pizzas  
- ☑️ Basic REST API available at `/api/GetPizzas`  
- ⬜ Dashboard for business intelligence using Python  
- ⬜ Online ordering system  
- ⬜ Customer authentication  
- ⬜ User shopping cart  
- ⬜ Email notifications  

---

## 🛠 Technologies

- **Django 5.2**
- **HTML / CSS**
- **SQLite** (default database)

---

## Installation

```bash
git clone https://github.com/youraccount/pizzamama.git
cd pizzamama
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Main Data Model

```python
class Pizza(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.CharField(max_length=400)
    price = models.FloatField(default=0)
    vegetarian = models.BooleanField(default=False)

    def __str__(self):
        return self.name
```

---

## 🔗 Live Demo

You can access the live version of PizzaMama here:  
👉 [https://fabricedeveloper.pythonanywhere.com](https://fabricedeveloper.pythonanywhere.com)

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve **PizzaMama**, please follow these simple steps:

1. **Fork** the repository  
2. **Create** a new branch (`git checkout -b feature/my-feature`)  
3. **Commit** your changes (`git commit -am 'Add some feature'`)  
4. **Push** to the branch (`git push origin feature/my-feature`)  
5. **Create a Pull Request**

Please make sure your code follows the style of the project and includes appropriate tests and documentation when relevant.

---

## 👤 Author

**Fabrice Ghislain Tebou**  
📧 ghislaintebou@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/fabrice-ghislain-tebou-72000b211/)

