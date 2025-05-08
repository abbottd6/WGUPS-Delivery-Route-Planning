from services.package_data_parser import package_keys
from services.package_data_parser import package_hash_table
from utils import custom_hash_table

def prompt_for_package_id():
    user_input = input("Enter Package ID: ")
    while int(user_input) < 1 or int(user_input) > len(package_keys):
        print("\n******************")
        print("Invalid Package ID")
        print("******************\n")
        user_input = input("Please enter a valid package ID (1-40), or 'm' to return to main menu:\n")
        if user_input.lower() == 'm':
            return
        elif user_input.isalpha() or int(user_input) < 1 or int(user_input) > len(package_keys):
            print("\nInvalid Package ID. Returning to main menu.\n")
            return
        else:
            break

    package_id = int(user_input)
    print(package_hash_table.get(package_id))
