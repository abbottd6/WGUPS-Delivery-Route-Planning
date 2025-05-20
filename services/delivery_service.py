from datetime import datetime, timedelta, date

from entities.route import Route
from entities.truck import Truck
from services.batch_truck_load_service import batch_truck_load_service
from services.distance_matrix_builder import distance_matrix_builder
from services.nearest_neighbor_path_generator import nearest_neighbor_path_generator
from services.package_priority_parsing_service import package_priority_parsing_service
from utils.calc_travel_time_minutes import calc_travel_time_minutes

today = date.today()
TIME_FORMAT = "%I:%M %p"
fmt = "%H:%M"
TRUCK_SPEED = 18
time_for_address_correction = datetime.strptime("10:20 AM", TIME_FORMAT).time()
PACKAGE_9_CORRECTION_TIME = datetime.combine(today, time_for_address_correction)
temp_truck1_time = datetime.strptime("8:00 AM", TIME_FORMAT).time()
TRUCK1_START_TIME = datetime.combine(today, temp_truck1_time)
temp_truck2_time = datetime.strptime("09:05 AM", TIME_FORMAT).time()
TRUCK2_START_TIME = datetime.combine(today, temp_truck2_time)

# Generate route data for delivery service
def start_delivery_service(all_package_keys, all_package_hash_table):

    route_objects = package_priority_parsing_service(all_package_keys, all_package_hash_table)

    return route_objects

def print_route_data(route_objects, route_number):
    print(route_objects[route_number])

# Function for running a simulation of delivery process and returning values depending on user input time
def query_delivery_service(time, route_objects, condition_code):
    try:
        temp_parsed_time = datetime.strptime(time, TIME_FORMAT).time()
        parsed_input_time = datetime.combine(today, temp_parsed_time)
    except ValueError:
        print(f"Time must be in format HH:MM AM/PM, e.g. '02:30 PM'.")
        return

    all_trucks = Truck.trucks_dict
    truck1 = all_trucks[1]
    truck2 = all_trucks[2]
    truck3 = all_trucks[3]

    all_trucks_elapsed_time = 0

    # CREATE COPIES OF ROUTE SPECIFIC HASH TABLES FOR STATUS ALTERATIONS
    this_temp_routes = route_objects.copy()

    # Calculate route completion times for trucks 1 and 2 to get truck 3 start time;
    # waiting for an available driver.
    constrained_route_complete_time = TRUCK2_START_TIME + timedelta(minutes=this_temp_routes[1].duration)
    priority_route_complete_time = TRUCK1_START_TIME + timedelta(minutes=this_temp_routes[0].duration)

    # Format complete times to remove the seconds/microseconds and round up by one minute
    constrained_route_complete_time = (constrained_route_complete_time.replace(second=0, microsecond=0)
                                       + timedelta(minutes=1))
    priority_route_complete_time = (priority_route_complete_time.replace(second=0, microsecond=0) +
                                    timedelta(minutes=1))

    # Set truck3_start_time to lesser/earlier time between truck 1 and truck 2 completion times
    temp_truck3_time = min(constrained_route_complete_time, priority_route_complete_time) + timedelta(minutes=1)
    truck3_start_time = datetime.combine(today, (temp_truck3_time.time()))

    truck1.route_start_time = TRUCK1_START_TIME
    truck2.route_start_time = TRUCK2_START_TIME
    truck3.route_start_time = truck3_start_time

    standard_route_complete_time = truck3_start_time + timedelta(minutes=this_temp_routes[2].duration)
    standard_route_complete_time = (standard_route_complete_time.replace(second=0, microsecond=0)
                                       + timedelta(minutes=1))

    route_completion_times = [priority_route_complete_time, constrained_route_complete_time,
                              standard_route_complete_time]

    # Calculate the amount of time each truck has been on route for delivery
    # from truck-specific start time, up to user input time
    for i, truck in enumerate(all_trucks.values(), start=0):
        time_dif = parsed_input_time - truck.route_start_time
        truck.en_route_time = time_dif.total_seconds() / 60.0

        if truck.route_start_time > parsed_input_time:
            for package in truck.packages:
                if "Delayed on flight" in package.notes:
                    package.status = "Delayed on flight"

        if (parsed_input_time >= PACKAGE_9_CORRECTION_TIME) and truck == truck3:
            for package in truck.packages:
                if package.package_id == 9:
                    package_no_9 = package
                    break
            if "Wrong address" in package_no_9.notes:
                package_no_9.update(
                    address="410 S State St",
                    city="Salt Lake City",
                    state="UT",
                    zip_code="84111",
                    deadline="EOD",
                    weight=2,
                    notes="Address corrected at 10:20 AM"
                )
                corrected_route_available = False
                for route in this_temp_routes:
                    if route.label == "Standard Packages":
                        incorrect_route = route

                        temp_route_keys = route.package_keys
                        temp_route_table = route.package_table
                        temp_route_matrix = distance_matrix_builder(temp_route_keys, temp_route_table)
                        updated_standard_route = nearest_neighbor_path_generator(temp_route_keys, temp_route_table,
                                                                                 temp_route_matrix)
                        updated_max_key = max(updated_standard_route.keys())
                        updated_route_distance = updated_standard_route[updated_max_key]["distance"]
                        updated_route_duration = calc_travel_time_minutes(updated_route_distance)

                        print(updated_standard_route)

                        updated_route_object = Route(
                            label="Standard Packages",
                            package_keys=temp_route_keys,
                            package_table=temp_route_table,
                            num_destinations=len(temp_route_matrix[0]) - 1,
                            distance_matrix=temp_route_matrix,
                            metadata=updated_standard_route,
                            total_distance=updated_route_distance,
                            duration=updated_route_duration,
                        )
                        corrected_route_available = True
                if corrected_route_available:
                    this_temp_routes.remove(incorrect_route)
                    this_temp_routes.append(updated_route_object)
                    truck3.packages.clear()
                    batch_truck_load_service(updated_standard_route, updated_route_object.package_keys,
                                             updated_route_object.package_table,
                                             "standard batch")






        # If the truck en_route_time (or time_dif) is less than zero, then the truck has not left the hub
        if 0 < truck.en_route_time:
            truck.status = "en route"
            # Set truck driver based on route number
            if i == 0 or i == 2:
                truck.driver_id = 1
            elif i == 1:
                truck.driver_id = 2
            # If the duration of the route is greater than zero but
            # less than the elapsed time since the truck left the hub,
            # then the truck has already traveled the total route distance
            if this_temp_routes[i].duration <= truck.en_route_time:
                truck.distance_traveled = this_temp_routes[i].total_distance
                truck.en_route_time = this_temp_routes[i].duration
            # Otherwise, if the route duration is greater than the amount of time the truck
            # has been on route, then it has only partially completed the route.
            else:
                # Truck distance traveled can be computed using the route time in hours, times the truck speed
                truck.distance_traveled = (truck.en_route_time / 60) * TRUCK_SPEED

        # If input time is after the completion time for the route, then the route has been completed
        # and the truck returned to the hub.
        if parsed_input_time > route_completion_times[i]:
            truck.status = "Returned to Hub"
            all_trucks_elapsed_time = all_trucks_elapsed_time + truck.en_route_time
            truck.driver_id = None

        # If the en route time for the truck is less than zero, then it has not left the hub yet.
        elif time_dif <= timedelta(0):
            truck.distance_traveled = 0
            truck.en_route_time = 0

    # Calculate the statuses of all packages at user input time.
    # Loop through all Trucks.
    for i, truck in enumerate(all_trucks.values(), start=0):
        # If the truck has left the Hub
        if truck.en_route_time > 0:
            # Loop through all destinations for a given truck
            for destination in this_temp_routes[i].metadata.values():
                if destination["distance"] <= truck.distance_traveled:
                    # Loop through all packages on this truck to find all packages associated with this address
                    for package in truck.packages:
                        # If, by user input time, the given truck has traveled far enough to have reached the
                        # package of this loop iteration, then the package has been delivered.
                        if destination["address"] in package.address:
                            # Calculate the elapsed time from truck departure to delivery of packages for this address.
                            en_route_time_to_delivery = calc_travel_time_minutes(destination["distance"])
                            # Calculate the delivery time of packages associated with this address.
                            package_delivery_time = (truck.route_start_time + timedelta(minutes=en_route_time_to_delivery))
                            # Set the package status of each package at this address to the calculated delivery time.
                            package.status = "Delivered: " + datetime.strftime(package_delivery_time, TIME_FORMAT)
                # If the truck has not traveled far enough to reach this loop iteration destination, the package
                # has not been delivered yet.
                # If this point in the control structure has been reached, then the package is out for delivery.
                # Set the status of the packages associated with this destination to en route
                elif destination["distance"] > truck.distance_traveled:
                    for package in truck.packages:
                        if destination["address"] in package.address:
                            package.status = "Package en route: Truck #" + str(truck.truck_id)

    # Check input condition_code to determine query response
    # IF CONDITION_CODE == 1
    if condition_code == 1:

        all_truck_hours = int(all_trucks_elapsed_time / 60)
        all_truck_mins = int(all_trucks_elapsed_time % 60)

        for truck in all_trucks.values():
            print(truck)
        print("TOTAL DELIVERY MILEAGE: ", truck1.distance_traveled + truck2.distance_traveled
              + truck3.distance_traveled, "miles\n")
        print("TOTAL DRIVER TIME (CONCURRENT): ", all_truck_hours, "hours and", all_truck_mins, "minutes\n")

    # IGNORE CONDITION_CODE 2, ITS HANDLED ELSEWHERE
    if condition_code == 2:
        return

    # IF CONDITION_CODE == 3
    if condition_code == 3:
        requested_package = int(input("Input package number (1-40):\n"))
        for truck in all_trucks.values():
            for package in truck.packages:
                if requested_package == package.package_id:
                    print("Package requested: \n", package)

    # IF CONDITION_CODE == 4
    if condition_code == 4:
        for truck in all_trucks.values():
            print(truck)

    # IGNORE CONDITION_CODE 5, ITS HANDLED ELSEWHERE
    if condition_code == 5:
        return

    if condition_code == 6:
        exit(1)


