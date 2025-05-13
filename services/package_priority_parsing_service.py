from services.distance_matrix_builder import distance_matrix_builder
from services.nearest_neighbor_path_generator import nearest_neighbor_path_generator
from services.print_all_packages import print_all_packages
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

    distance_matrix_builder(priority_package_keys, priority_delivery_package_table)


