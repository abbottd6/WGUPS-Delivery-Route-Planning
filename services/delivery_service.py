from datetime import datetime, timedelta

from entities.truck import Truck
from services.nearest_neighbor_path_generator import nearest_neighbor_path_generator
from services.package_priority_parsing_service import package_priority_parsing_service

TIME_FORMAT = "%I:%M %p"
fmt = "%H:%M"
TRUCK_SPEED = 18
TRUCK1_START_TIME = datetime.strptime("8:00 AM", TIME_FORMAT)
TRUCK2_START_TIME = datetime.strptime("09:05 AM", TIME_FORMAT)


def start_delivery_service(all_package_keys, all_package_hash_table, all_distance_matrix):

    route_objects = package_priority_parsing_service(all_package_keys, all_package_hash_table)

    # for route in route_objects:
    #     print(route)

    # for truck in Truck.trucks_dict.values():
    #     print(truck)
    return route_objects

def print_route_data(route_objects, route_number):
    print(route_objects[route_number])

def query_delivery_service(time, route_objects, condition_code):
    try:
        parsed_input_time = datetime.strptime(time, TIME_FORMAT)
    except ValueError:
        print(f"Time must be in format HH:MM AM/PM, e.g. '02:30 PM'.")
        return

    all_trucks = Truck.trucks_dict
    truck1 = all_trucks[1]
    truck2 = all_trucks[2]
    truck3 = all_trucks[3]

    # Retrieve individual routes and respective distances
    priority_route = route_objects[0]
    priority_total_distance = priority_route.total_distance

    constrained_route = route_objects[1]
    constrained_total_distance = constrained_route.total_distance

    standard_route = route_objects[2]
    standard_total_distance = standard_route.total_distance

    # -------------------- TO DO ------------------------
    # Calculate route completion times for trucks 1 and 2 to get truck 3 start time;
    # waiting for an available driver.
    constrained_route_complete_time = TRUCK2_START_TIME + timedelta(minutes=constrained_route.duration)

    # CALCULATE TRUCK 1 COMPLETION TIME

    # COMPARE TRUCK 1 & 2 COMPLETION TIMES

    # -------------------- TO DO ------------------------
    # SET TRUCK 3 START TIME TO LESSER OF TRUCK 1 AND TRUCK 2 COMPLETION TIMES


    truck3_start_time = constrained_route_complete_time.time()

    # -------------------- TO DO ------------------------
    # CREATE COPIES OF ROUTE SPECIFIC HASH TABLES FOR STATUS ALTERATIONS

    # Calculate the amount of time that each truck has been on route for delivery
    # from truck-specific start time, up to user input time
    truck1_time_dif = parsed_input_time - TRUCK1_START_TIME
    truck1_en_route_time = (truck1_time_dif.total_seconds() / 60.0) / 60.0
    if parsed_input_time - TRUCK1_START_TIME >= timedelta(minutes=0):
        for package in truck1.packages:
            # NEED TO DO THIS IN THE COPIED HASH TABLE, NOT JUST THE TRUCK?
            package.status("En Route")
        if priority_route.duration <= truck1_en_route_time:
            truck1_distance_traveled = priority_route.total_distance
        else:
            truck1_distance_traveled = truck1_en_route_time * TRUCK_SPEED
    else:
        truck1_distance_traveled = 0


    truck2_time_dif = parsed_input_time - TRUCK2_START_TIME
    truck2_delivery_minutes = (truck2_time_dif.total_seconds() / 60.0)
    truck2_delivery_hours = (truck2_delivery_minutes / 60.0)
    if parsed_input_time - TRUCK2_START_TIME <= timedelta(minutes=0):
        truck2_distance_traveled = 0
    if constrained_route.duration <= truck2_delivery_hours:
        truck2_distance_traveled = constrained_route.total_distance
    else:
        truck2_distance_traveled = truck2_delivery_hours * TRUCK_SPEED

    # -------------------- TO DO ------------------------
    # Calculate the amount of time that truck 3 has been on route up to given user time
    # truck3_time_dif = parsed_input_time - TRUCK2_START_TIME
    # truck3_delivery_minutes = (truck3_time_dif.total_seconds() / 60.0)
    # truck3_delivery_hours = (truck2_delivery_minutes / 60.0)
    # truck3_distance_traveled = truck3_delivery_hours * TRUCK_SPEED

    # FOR TRUCK IN Truck.trucks_dict (1-3)
        # IF ON ROUTE TIME > 0.
            # FOR DESTINATION IN ROUTE.DESTINATIONS:
                # IF TIME TO THIS.PACKAGE DELIVERY < ACTUAL ON ROUTE TIME RELATIVE TO USER INPUT TIME AND START TIME
                    # ADD ON ROUTE TIME REQUIRED (TO REACH ITERATION SPECIFIC DESTINATION) TO TRUCK SPECIFIC START TIME
                    # TO GET DELIVERY_TIME
                    # GET TRUCK.PACKAGES ADDRESS ASSOCIATED PACKAGES
                    # FOR PACKAGE IN ASSOCIATED PACKAGES
                        # SET PACKAGE STATUS TO ("Delivered at: ", DELIVERY_TIME)

    # CHECK INPUT CONDITION CODE TO DETERMINE QUERY RESPONSE
    # IF CONDITION_CODE == 1
        # RETURN PARENT HASH TABLE FOR EOD
            # WITH INDIVIDUAL TRUCK EN ROUTE TIMES
            # INDIVIDUAL ROUTE TOTAL DISTANCES
            # COMBINED TOTAL DISTANCE FOR ALL TRUCKS

    # IGNORE CONDITION_CODE 2, ITS HANDLED ELSEWHERE

    # IF CONDITION_CODE == 3
        # GET USER_INPUT FOR PACKAGE NUMBER
        # RETURN PACKAGE METADATA AT PROVIDED TIME

    # IF CONDITION_CODE == 4
        # RETURN ALL PACKAGE METADATA AT PROVIDED TIME

    # IGNORE CONDITION_CODE 5, ITS HANDLED ELSEWHERE

    # print("Priority Route Total Distance: ", priority_total_distance)
    #
    # print(f"Truck 1 Distance: {truck1_distance_traveled}")
    # print(f"Truck 2 Distance: {truck2_distance_traveled}")


