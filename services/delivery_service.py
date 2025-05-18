from datetime import datetime, timedelta, date

from entities.truck import Truck
from services.package_priority_parsing_service import package_priority_parsing_service
from utils.calc_travel_time_minutes import calc_travel_time_minutes

today = date.today()
TIME_FORMAT = "%I:%M %p"
fmt = "%H:%M"
TRUCK_SPEED = 18
temp_truck1_time = datetime.strptime("8:00 AM", TIME_FORMAT).time()
TRUCK1_START_TIME = datetime.combine(today, temp_truck1_time)
temp_truck2_time = datetime.strptime("09:05 AM", TIME_FORMAT).time()
TRUCK2_START_TIME = datetime.combine(today, temp_truck2_time)

def start_delivery_service(all_package_keys, all_package_hash_table, all_distance_matrix):

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
            truck.driver_id = None

        # If the en route time for the truck is less than zero, then it has not left the hub yet.
        # elif time_dif <= timedelta(0):
        #     truck.distance_traveled = 0
        #     truck.en_route_time = 0

    # for truck in all_trucks.values():
    #     print(truck)

    for i, truck in enumerate(all_trucks.values(), start=0):
        if truck.en_route_time > 0:
            for destination in this_temp_routes[i].metadata.values():
                if destination["distance"] <= truck.distance_traveled:
                    for package in truck.packages:
                        if destination["address"] in package.address:
                            en_route_time_to_delivery = calc_travel_time_minutes(destination["distance"])
                            package_delivery_time = (truck.route_start_time + timedelta(minutes=en_route_time_to_delivery))
                            package.status = "Delivered: " + datetime.strftime(package_delivery_time, TIME_FORMAT)
                elif destination["distance"] > truck.distance_traveled:
                    for package in truck.packages:
                        if destination["address"] in package.address:
                            package.status = "Package en route"

    for truck in all_trucks.values():
        print(truck)
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


