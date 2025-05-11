import os
from datetime import datetime

while True:
    path_folder = input("Insert the path of the folder (or press 'q' to quit): ").strip()
    
    if path_folder.lower() == 'q':
        print("You have chosen to quit the program. Thank you.")
        break
               
    if not os.path.exists(path_folder):
        print("The folder path is not valid. Please try again.")
        continue
    
    while True:
        print("\nMenu options:")
        print("1. Check the properties of all the folders.")
        print("2. Check the properties of the files.")
        print("3. Check properties of both kinds of elements.")
        print("0. Quit the program")
            
        choice_user = input("\nInsert the number according to your choice: ").strip()
        
        if choice_user not in ['0', '1', '2', '3']:
            print("Invalid choice. Please try again.")
            continue
            
        # Collect elements
        folders = []
        files = []
        for element in os.listdir(path_folder):
            full_path = os.path.join(path_folder, element)
            size = os.path.getsize(full_path)
            date = datetime.fromtimestamp(os.path.getctime(full_path))
            
            if os.path.isfile(full_path):
                files.append((element, size, date))
            else: 
                folders.append((element, size, date))
        
        # Process choice
        if choice_user == "0":
            print("Exiting program...")
            exit()
        
        header = "name, size(bytes), date creation"
        
        if choice_user == "1":
            print("\nFolders:")
            print(header)
            for name, size, date in folders:
                print(f"{name}, {size}, {date}")
        
        elif choice_user == "2":
            print("\nFiles:")
            print(header)
            for name, size, date in files:
                print(f"{name}, {size}, {date}")
        
        elif choice_user == "3":
            print("\nFolders:")
            print(header)
            for name, size, date in folders:
                print(f"{name}, {size}, {date}")
            
            print("\nFiles:")
            print(header)
            for name, size, date in files:
                print(f"{name}, {size}, {date}")
        
        if input("\nMake another choice? (y/n): ").lower() != 'y':
            break