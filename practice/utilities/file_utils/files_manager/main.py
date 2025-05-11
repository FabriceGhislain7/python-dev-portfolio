import os
from datetime import datetime

while True:
    path_folder = input("Insert the path of the folder (or press 'q' to quit): ").strip()
    
    if path_folder == 'q':
        print("You have chosen to quit the program. Thank you.")
        break
               
    if not os.path.exists(path_folder):
        print("The folder path is not valid. Please try again.")
        continue
    
    while True:
        choice_menu = {
            "1": "Check the properties of all the folders.",
            "2": "Check the properties of the files.",
            "3": "Check properties of both kinds of elements.",
            "0": "Quit the program"
        }
        
        print("\nMenu options:")
        for key, value in choice_menu.items():
            print(f"{key}. {value}")
            
        choice_user = input("\nInsert the number according to your choice: ")
        
        if choice_user not in choice_menu.keys():
            print("The number entered for the choice is not valid. Please try again.")
            continue
            
        list_folders = []
        list_files = []
        
        for element in os.listdir(path_folder):
            path_element = os.path.join(path_folder, element)     
            size_element = os.path.getsize(path_element) 
            date_creation_element = datetime.fromtimestamp(os.path.getctime(path_element))
            
            if os.path.isfile(path_element):
                list_files.append([element, size_element, date_creation_element])
            else: 
                list_folders.append([element, size_element, date_creation_element])
        
        if choice_user == "0":
            print("You have chosen to quit the program.")
            exit()
        elif choice_user == "1":
            print("\nAll folders in the given folder:")
            print("name, size(bytes), date creation")  # Header line
            for elt_fold in list_folders:
                print(f"{elt_fold[0]}, {elt_fold[1]}, {elt_fold[2]}")
        elif choice_user == "2":
            print("\nAll files in the given folder:")
            print("name, size(bytes), date creation")  # Header line
            for elt_file in list_files:
                print(f"{elt_file[0]}, {elt_file[1]}, {elt_file[2]}")
        elif choice_user == "3":
            print("\nAll elements in the given folder:")
            print("\nFolders:")
            print("name, size(bytes), date creation")  # Header line
            for elt_fold in list_folders:
                print(f"{elt_fold[0]}, {elt_fold[1]}, {elt_fold[2]}")
            print("\nFiles:")
            print("name, size(bytes), date creation")  # Header line
            for elt_file in list_files:
                print(f"{elt_file[0]}, {elt_file[1]}, {elt_file[2]}")
        
        another_choice = input("\nDo you want to make another choice? (y/n): ").lower()
        if another_choice != 'y':
            break