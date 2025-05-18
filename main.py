from entities.truck import Truck
from services.delivery_service import start_delivery_service, query_delivery_service, print_route_data
from services.package_data_parser import package_keys, package_hash_table, distance_matrix
from UI_components.prompt_for_package_id import prompt_for_package_id
from UI_components.main_menu import main_menu
from utils.instantiate_delivery_infra import instantiate_delivery_infra

exit_delivery_monitor = False
line_format = ""

while not exit_delivery_monitor:

    main_menu()

    user_input = input()

    # Print all package status and mileage
    # when deliveries are completed
    if user_input == '1':
        instantiate_delivery_infra()
        routes = start_delivery_service(package_keys, package_hash_table)

        query_delivery_service("6:00 PM", routes, int(user_input))

    # Print single package info by ID
    if user_input == '2':
        instantiate_delivery_infra()
        routes = start_delivery_service(package_keys, package_hash_table)

        prompt_for_package_id()

    # Get single package status at a given time
    if user_input == '3':
        instantiate_delivery_infra()
        routes = start_delivery_service(package_keys, package_hash_table)

        user_time = input("Enter time in format: HH:MM AM/PM\n (space between time and AM/PM)\n")
        query_delivery_service(user_time, routes, 3)

    # Get all package statuses at given time
    if user_input == '4':
        instantiate_delivery_infra()
        routes = start_delivery_service(package_keys, package_hash_table)

        user_time = input("Enter time in format: HH:MM:AM/PM\n (space between time and AM/PM)\n")
        query_delivery_service(user_time, routes, 4)

    # print route data based on truck number
    if user_input == '5':
        instantiate_delivery_infra()
        routes = start_delivery_service(package_keys, package_hash_table)

        route_number = int(input("Enter route number (1-3)\n"))
        print(Truck.trucks_dict[route_number])
        print_route_data(routes, route_number - 1)

    # Exit program
    if user_input == '6':
        exit_delivery_monitor = True