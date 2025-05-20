from entities.truck import Truck
from services.delivery_service import start_delivery_service, query_delivery_service, print_route_data
from services.package_data_parser import package_keys, package_hash_table, distance_matrix
from UI_components.prompt_for_package_id import prompt_for_package_id
from UI_components.main_menu import main_menu
from utils.instantiate_delivery_infra import instantiate_delivery_infra

#Dayton Abbott
#011125353

line_format = ""

def get_fresh_routes():
    instantiate_delivery_infra()
    routes = start_delivery_service(package_keys, package_hash_table)
    return routes

def main():

    exit_delivery_monitor = False

    while not exit_delivery_monitor:

        main_menu()
        routes = get_fresh_routes()

        user_input = input()

        # Print all package status and mileage
        # when deliveries are completed
        if user_input == '1':
            query_delivery_service("6:00 PM", routes, int(user_input))

        # Print single package info by ID
        elif user_input == '2':
            prompt_for_package_id()

        # Get single package status at a given time
        elif user_input == '3':
            user_time = input("Enter time in format: HH:MM AM/PM\n (space between time and AM/PM)\n")
            query_delivery_service(user_time, routes, 3)

        # Get all package statuses at given time
        elif user_input == '4':
            user_time = input("Enter time in format: HH:MM:AM/PM\n (space between time and AM/PM)\n")
            query_delivery_service(user_time, routes, 4)

        # print route data based on truck number
        elif user_input == '5':
            route_number = int(input("Enter route number (1-3)\n"))
            print(Truck.trucks_dict[route_number])
            print_route_data(routes, route_number - 1)

        # Exit program
        elif user_input == '6':
            exit_delivery_monitor = True

        else:
            print("Invalid input. Please try again.")

if __name__ == '__main__':
    main()