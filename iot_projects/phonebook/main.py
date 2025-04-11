import os
from datetime import datetime
import shutil

phonebook = {}  # Using a clearer variable name

# --------------- Create the phonebook file if it doesn't exist ---------------
phonebook_file = "phonebook.txt"
if not os.path.exists(phonebook_file):
    with open(phonebook_file, "w", encoding="utf-8") as file:
        file.write("code,last_name,first_name,phone_number,email,creation_date")

# --------------- Load existing contacts into memory ---------------
with open(phonebook_file, "r", encoding="utf-8") as file:
    for line in file:
        code, last_name, first_name, phone_number, email, creation_date = line.strip().split(",")
        phonebook[code] = {
            "Last Name": last_name,
            "First Name": first_name,
            "Phone": phone_number,
            "Email": email,
            "Created On": creation_date
        }

# --------------- Main Menu Loop ---------------
while True:
    menu_options = {
        "1": "View all contacts",
        "2": "Add/Edit/Delete a contact",
        "3": "Search contacts",
        "4": "Backup phonebook",
        "0": "Exit"
    }

    # Display menu
    print(f"{'PHONEBOOK MENU':^40}\n{'=' * 40}")
    for option, description in menu_options.items():
        print(f"{option}: {description}")

    user_choice = input("Select an option: ").strip()       # Get user choice

    # Process choice using match-case
    match user_choice:
        case "0": 
            print("Exiting the program. Goodbye!")
            break 

        case "1":  # View all contacts
            print("\nAll Contacts:")
            for contact_id, details in phonebook.items():
                print(f"\nID: {contact_id}")
                for key, value in details.items():
                    print(f"{key}: {value}")

        case "2":  
            print("\nContact Management")
            # Your code for adding/editing/deleting goes here

        case "3":  # Search
            print("\nContact Search")
            # Your search functionality goes here

        case "4":  # Backup
            print("\nCreating Backup...")
            # Your backup logic goes here

        case _:  # Invalid option
            print("\nError: Invalid choice. Please select 0-4.")