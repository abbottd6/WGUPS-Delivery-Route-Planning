from UI_components.print_route_metadata import print_route_metadata
from entities.route import Route
from entities.truck import Truck
from services.delivery_batch_builder import delivery_batch_builder
from services.distance_matrix_builder import distance_matrix_builder
from services.nearest_neighbor_path_generator import nearest_neighbor_path_generator
from utils.calc_travel_time import calc_travel_time
from UI_components.print_all_packages import print_all_packages
from utils.custom_hash_table import PackageHashTable

def package_priority_parsing_service(some_package_keys, some_package_hash_table):

    # Create arrays for three separate package priority classifications.
    priority_package_keys = []
    constrained_package_keys = []
    standard_package_keys = []

    # Use package_id from package_keys to loop through all packages to determine
    # package priority classification.
    for package_id in some_package_keys:
        temp_package = some_package_hash_table.get_by_id(package_id)
        # if a package has any delivery note, then it is a constrained package.
        if temp_package.notes:
            constrained_package_keys.append(package_id)
        # If a package has a delivery deadline, and the package is not already
        # in constrained packages, then it is assigned to the priority packages array.
        if "EOD" not in temp_package.deadline:
            if package_id in constrained_package_keys:
                continue
            else:
                priority_package_keys.append(package_id)
        # If a package is neither assigned to constrained packages nor priority packages,
        # then it is a standard package.
        if package_id not in constrained_package_keys and package_id not in priority_package_keys:
            # There are too many standard packages to fit on one truck,
            # so standard packages are assigned to standard package array, so long as the
            # number of packages in standard packages does not exceed truck capacity.
            # When the standard package array reaches maximum size, the remaining standard
            # packages are dispersed between priority and constrained package arrays
            if len(standard_package_keys) < 16:
                standard_package_keys.append(package_id)
            elif len(priority_package_keys):
                priority_package_keys.append(package_id)
            elif len(constrained_package_keys):
                constrained_package_keys.append(package_id)

    # Create hash tables for each package classification array based on the size of the array
    constrained_delivery_package_table = PackageHashTable(len(constrained_package_keys))
    priority_delivery_package_table = PackageHashTable(len(priority_package_keys))
    standard_delivery_package_table = PackageHashTable(len(standard_package_keys))

    # Take package classification arrays and build distinct hash tables for each classification
    for package_id in priority_package_keys:
        priority_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))
    for package_id in constrained_package_keys:
        constrained_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))
    for package_id in standard_package_keys:
        standard_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))

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
    delivery_batch_builder(priority_delivery_route, priority_package_keys,
                           priority_delivery_package_table, "priority batch")

    delivery_batch_builder(constrained_delivery_route, constrained_package_keys,constrained_delivery_package_table,
                           "constrained batch")

    delivery_batch_builder(standard_delivery_route, standard_package_keys, standard_delivery_package_table,
                           "standard batch")

    priority_route_object = Route(
        route_label="Priority Packages",
        route_package_keys=priority_package_keys,
        route_package_table=priority_delivery_package_table,
        route_num_destinations=len(priority_package_distance_matrix[0]) - 1,
        route_distance_matrix=priority_package_distance_matrix,
        route=priority_delivery_route
    )
    constrained_route_object = Route(
        route_label="Constrained Packages",
        route_package_keys=constrained_package_keys,
        route_package_table=constrained_delivery_package_table,
        route_num_destinations=len(constrained_package_distance_matrix[0]) - 1,
        route_distance_matrix=constrained_package_distance_matrix,
        route=constrained_delivery_route
    )
    standard_route_object = Route(
        route_label="Standard Packages",
        route_package_keys=standard_package_keys,
        route_package_table=standard_delivery_package_table,
        route_num_destinations=len(standard_package_distance_matrix[0]) - 1,
        route_distance_matrix=standard_package_distance_matrix,
        route = standard_delivery_route
    )

    route_objects = [priority_route_object, constrained_route_object, standard_route_object]

    # returning the dictionary of routes
    return route_objects





