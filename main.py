from services.delivery_batch_builder import delivery_batch_builder
from services.nearest_neighbor_path_generator import nearest_neighbor_path_generator
from services.print_all_packages import print_all_packages
from services.prompt_for_package_id import prompt_for_package_id
from services.main_menu import main_menu
from utils.instantiate_delivery_infra import instantiate_delivery_infra
from entities.truck import Truck

exit_delivery_monitor = False
line_format = ""

instantiate_delivery_infra()

route = nearest_neighbor_path_generator()
delivery_batch_builder(route)

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
        nearest_neighbor_path_generator()

    if user_input == '6':
        exit_delivery_monitor = True