import copy

from entities.route import Route
from services.batch_truck_load_service import batch_truck_load_service
from services.distance_matrix_builder import distance_matrix_builder
from services.nearest_neighbor_path_generator import nearest_neighbor_path_generator
from utils.calc_travel_time_minutes import calc_travel_time_minutes
from utils.custom_hash_table import PackageHashTable

def package_priority_parsing_service(some_package_keys, some_package_hash_table):

    instanced_package_hash_table = copy.deepcopy(some_package_hash_table)
    not_corrected = True

    # Create arrays for three separate package priority classifications.
    priority_package_keys = []
    constrained_package_keys = []
    standard_package_keys = []

    # Use package_id from package_keys to loop through all packages to determine
    # package priority classification.
    for package_id in some_package_keys:
        temp_package = instanced_package_hash_table.get_by_id(package_id)
        # if a package has any delivery note, then it is a constrained package.
        if temp_package.notes and not "Wrong address" in temp_package.notes:
            constrained_package_keys.append(package_id)
        # If a package has a delivery deadline, and the package is not already
        # in constrained packages, then it is assigned to the priority packages array.
        elif not temp_package.notes and not temp_package.deadline[0].isalpha():
            if package_id not in constrained_package_keys and package_id not in standard_package_keys:
                association_check = instanced_package_hash_table.get_by_id(package_id)
                associated_packages = instanced_package_hash_table.get_by_address(association_check.address)
                if len(priority_package_keys) + len(associated_packages) <= 16:
                    for package in associated_packages:
                        if package.notes:
                            continue
                        if package.package_id not in priority_package_keys and package.package_id not in standard_package_keys:
                            priority_package_keys.append(package.package_id)
        # If a package is neither assigned to constrained packages nor priority packages,
        # then it is a standard package.
        else:
            if package_id not in constrained_package_keys and package_id not in priority_package_keys:
                # There are too many standard packages to fit on one truck,
                # so standard packages are assigned to standard package array, so long as the
                # number of packages in standard packages does not exceed truck capacity.
                # When the standard package array reaches maximum size, the remaining standard
                # packages are dispersed between priority and constrained package arrays
                if ((len(standard_package_keys) < 16) and (package_id not in priority_package_keys)
                        and (package_id not in constrained_package_keys)):
                    standard_package_keys.append(package_id)
                elif ((len(priority_package_keys) < 16) and (package_id not in priority_package_keys)
                      and (package_id not in constrained_package_keys)):
                    priority_package_keys.append(package_id)
                elif ((len(constrained_package_keys) < 16) and (package_id not in priority_package_keys)
                      and (package_id not in constrained_package_keys)):
                    constrained_package_keys.append(package_id)

    if not_corrected:
        package_to_correct = instanced_package_hash_table.get_by_id(9)
        package_to_correct.update(
            address="410 S State St",
            city="Salt Lake City",
            state="UT",
            zip_code="84111",
            deadline="EOD",
            weight=2,
            notes="Address corrected at 10:20 AM"
        )
        not_corrected = False

    # keys_comparison_check = priority_package_keys.copy()
    # keys_comparison_check.extend(constrained_package_keys)
    # keys_comparison_check.extend(standard_package_keys)
    # keys_comparison_check.sort()
    #
    # seen = set()
    # print(keys_comparison_check)
    # for package_id in keys_comparison_check:
    #     if package_id in seen:
    #         print("Package id " + str(package_id) + " is duplicated.")
    #     else:
    #         seen.add(package_id)
    # print("non duplicate count", len(seen))
    # print("duplicate count", len(keys_comparison_check))

    # Create hash tables for each package classification array based on the size of the array
    constrained_delivery_package_table = PackageHashTable(len(constrained_package_keys))
    priority_delivery_package_table = PackageHashTable(len(priority_package_keys))
    standard_delivery_package_table = PackageHashTable(len(standard_package_keys))

    # Take package classification arrays and build distinct hash tables for each classification
    for package_id in priority_package_keys:
        priority_delivery_package_table.insert(package_id, instanced_package_hash_table.get_by_id(package_id))
    for package_id in constrained_package_keys:
        constrained_delivery_package_table.insert(package_id, instanced_package_hash_table.get_by_id(package_id))
    for package_id in standard_package_keys:
        standard_delivery_package_table.insert(package_id, instanced_package_hash_table.get_by_id(package_id))

    # Take classification distinct package hash tables and generate distance matrices for packages
    # in that classification group
    priority_package_distance_matrix = distance_matrix_builder(priority_package_keys,
                                                             priority_delivery_package_table)
    constrained_package_distance_matrix = distance_matrix_builder(constrained_package_keys,
                                                                constrained_delivery_package_table)
    standard_package_distance_matrix = distance_matrix_builder(standard_package_keys,
                                                             standard_delivery_package_table)

    # Pass the distinct package classification data sets (keys, hash table, distance matrix)
    # into the nearest neighbor path generator to create a greedy delivery route
    priority_delivery_route = nearest_neighbor_path_generator(priority_package_keys, priority_delivery_package_table,
                                                              priority_package_distance_matrix)

    constrained_delivery_route = nearest_neighbor_path_generator(constrained_package_keys,
                                                                 constrained_delivery_package_table,
                                                                 constrained_package_distance_matrix)

    standard_delivery_route = nearest_neighbor_path_generator(standard_package_keys, standard_delivery_package_table,
                                                              standard_package_distance_matrix)

    # Take delivery route and load packages into truck
    batch_truck_load_service(priority_delivery_route, priority_package_keys,
                             priority_delivery_package_table, "priority batch")

    batch_truck_load_service(constrained_delivery_route, constrained_package_keys, constrained_delivery_package_table,
                           "constrained batch")

    batch_truck_load_service(standard_delivery_route, standard_package_keys, standard_delivery_package_table,
                           "standard batch")

    # Retrieve the max (last) key for each route to use for distance calculation
    priority_route_max_key = max(priority_delivery_route.keys())
    constrained_route_max_key = max(constrained_delivery_route.keys())
    standard_route_max_key = max(standard_delivery_route.keys())

    # Calculate total distances for routes
    priority_route_total_distance = priority_delivery_route[priority_route_max_key]["distance"]
    constrained_route_total_distance = constrained_delivery_route[constrained_route_max_key]["distance"]
    standard_route_total_distance = standard_delivery_route[standard_route_max_key]["distance"]

    # Calculate total route duration
    priority_route_duration = calc_travel_time_minutes(priority_route_total_distance)
    constrained_route_duration = calc_travel_time_minutes(constrained_route_total_distance)
    standard_route_duration = calc_travel_time_minutes(standard_route_total_distance)

    #

    priority_route_object = Route(
        label="Priority Packages",
        package_keys=priority_package_keys,
        package_table=priority_delivery_package_table,
        num_destinations=len(priority_package_distance_matrix[0]) - 1,
        distance_matrix=priority_package_distance_matrix,
        metadata=priority_delivery_route,
        total_distance=priority_route_total_distance,
        duration=priority_route_duration,
    )
    constrained_route_object = Route(
        label="Constrained Packages",
        package_keys=constrained_package_keys,
        package_table=constrained_delivery_package_table,
        num_destinations=len(constrained_package_distance_matrix[0]) - 1,
        distance_matrix=constrained_package_distance_matrix,
        metadata=constrained_delivery_route,
        total_distance=constrained_route_total_distance,
        duration=constrained_route_duration,
    )
    standard_route_object = Route(
        label="Standard Packages",
        package_keys=standard_package_keys,
        package_table=standard_delivery_package_table,
        num_destinations=len(standard_package_distance_matrix[0]) - 1,
        distance_matrix=standard_package_distance_matrix,
        metadata=standard_delivery_route,
        total_distance=standard_route_total_distance,
        duration=standard_route_duration,
    )

    route_objects = [priority_route_object, constrained_route_object, standard_route_object]

    # returning the dictionary of routes
    return route_objects





