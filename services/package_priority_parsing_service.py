from entities.truck import Truck
from services.delivery_batch_builder import delivery_batch_builder
from services.distance_matrix_builder import distance_matrix_builder
from services.nearest_neighbor_path_generator import nearest_neighbor_path_generator
from utils.calc_travel_time import calc_travel_time
from UI_components.print_all_packages import print_all_packages
from utils.custom_hash_table import PackageHashTable

def package_priority_parsing_service(some_package_keys, some_package_hash_table):

    priority_package_keys = []
    constrained_package_keys = []
    standard_package_keys = []

    for package_id in some_package_keys:
        temp_package = some_package_hash_table.get_by_id(package_id)
        if temp_package.notes:
            constrained_package_keys.append(package_id)
        if "EOD" not in temp_package.deadline:
            if package_id in constrained_package_keys:
                continue
            else:
                priority_package_keys.append(package_id)
        if package_id not in constrained_package_keys and package_id not in priority_package_keys:
            if len(standard_package_keys) < 16:
                standard_package_keys.append(package_id)
            elif len(priority_package_keys):
                priority_package_keys.append(package_id)
            elif len(constrained_package_keys):
                constrained_package_keys.append(package_id)

    constrained_delivery_package_table = PackageHashTable(len(constrained_package_keys))
    priority_delivery_package_table = PackageHashTable(len(priority_package_keys))
    standard_delivery_package_table = PackageHashTable(len(standard_package_keys))

    for package_id in priority_package_keys:
        priority_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))
    for package_id in constrained_package_keys:
        constrained_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))
    for package_id in standard_package_keys:
        standard_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))


        # temp_package = some_package_hash_table.get_by_id(package_id)
        # package_notes = temp_package.notes
        #
        # if package_notes:
        #     if "delivered with" in package_notes or "can only be on truck" in package_notes:
        #         constrained_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))
        #     if "delayed on flight" in package_notes:
        #         if "EOD" in some_package_hash_table.get(package_id).deadline:
        #             standard_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))
        #         else:
        #             priority_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))
        # else:
        #     if "EOD" in temp_package.deadline:
        #         standard_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))
        #     else:
        #         priority_delivery_package_table.insert(package_id, some_package_hash_table.get_by_id(package_id))

    print("\nPrio keys: ", priority_package_keys)
    print_all_packages(priority_package_keys, priority_delivery_package_table, "Priority Delivery Packages")

    print("\nConstrained Keys: ", constrained_package_keys)
    print_all_packages(constrained_package_keys, constrained_delivery_package_table, "Constrained Delivery Packages")

    print("\nStandard Keys: ", standard_package_keys)
    print_all_packages(standard_package_keys, standard_delivery_package_table, "Standard Delivery Packages")

    priority_package_distance_matrix = distance_matrix_builder(priority_package_keys,
                                                             priority_delivery_package_table)
    constrained_package_distance_matrix = distance_matrix_builder(constrained_package_keys,
                                                                constrained_delivery_package_table)
    standard_package_distance_matrix = distance_matrix_builder(standard_package_keys,
                                                             standard_delivery_package_table)

    priority_delivery_route = nearest_neighbor_path_generator(priority_package_keys, priority_delivery_package_table,
                                                              priority_package_distance_matrix)
    print(priority_delivery_route)
    total_distance = 0
    for destination in priority_delivery_route.values():
        if "4001 South 700 East" in destination["address"]:
            continue
        total_distance += destination["distance"]
    print("total distance: ", total_distance, "route duration: ", calc_travel_time(total_distance))

    # NEED TO ADJUST THE PRIORITY DELIVERY ORDER BECAUSE OF THE STUPID ONE THAT HAS TO BE DELIVERED BY 9

    constrained_delivery_route = nearest_neighbor_path_generator(constrained_package_keys,
                                                                 constrained_delivery_package_table,
                                                                 constrained_package_distance_matrix)
    standard_delivery_route = nearest_neighbor_path_generator(standard_package_keys, standard_delivery_package_table,
                                                              standard_package_distance_matrix)

    delivery_batch_builder(priority_delivery_route, priority_package_keys,
                           priority_delivery_package_table, "priority batch")

    delivery_batch_builder(constrained_delivery_route, constrained_package_keys,constrained_delivery_package_table,
                           "constrained batch")

    delivery_batch_builder(standard_delivery_route, standard_package_keys, standard_delivery_package_table,
                           "standard batch")

    for truck in Truck.trucks_dict.values():
        print(truck)



