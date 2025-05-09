from services.print_all_packages import print_all_packages
from services.print_dist_matrix import print_dist_matrix
from services.prompt_for_package_id import prompt_for_package_id
from services.main_menu import main_menu

exit_delivery_monitor = False
line_format = ""

print_all_packages()
print_dist_matrix()


while not exit_delivery_monitor:
    main_menu()

    user_input = input()

    if user_input == '1':
        print_all_packages()

    if user_input == '2':
        prompt_for_package_id()

    if user_input == '3':
        user_time = input("Enter time in format: HH:MM:SS\n")
        #NEEDS TO BE COMPLETED
    if user_input == '4':
        user_time = input("Enter time in format: HH:MM:SS\n")
        # NEEDS TO BE COMPLETED
    if user_input == '5':
        exit_delivery_monitor = True