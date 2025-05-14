from entities.truck import Truck
from collections import deque

def delivery_batch_builder(route_path, some_package_keys, some_package_hash_table, label):
    total_package_count = 0
    batch = deque()
    batch_package_count = 0
    package_match_count = 0
    carryover_packages = []

    if "priority batch" in label:
        truck_number = 1
    elif "constrained batch" in label:
        truck_number = 2
    elif "standard batch" in label:
        truck_number = 3
    else:
        truck_number = 4

    for delivery_stop in route_path.values():
        if carryover_packages:
            for carryover_package in carryover_packages:
                batch.append(carryover_package)
                batch_package_count += 1
                total_package_count += 1
            carryover_packages = []

        address_associated_packages = some_package_hash_table.get_by_address(delivery_stop["address"])
        package_match_count += len(address_associated_packages)

        if len(address_associated_packages) == 0:
            continue
        if (batch_package_count + len(address_associated_packages) <= 16) and total_package_count < len(some_package_keys):
            for package in address_associated_packages:
                    batch.append(some_package_hash_table.get_by_id(package.package_id))
                    batch_package_count += 1
                    total_package_count += 1
            can_load_more = True
        else:
            can_load_more = False
            for package in address_associated_packages:
                carryover_packages.append(some_package_hash_table.get_by_id(package.package_id))
        if (batch_package_count == 16) or (package_match_count == len(some_package_keys)) or can_load_more == False:

            # print("\nTruck number: ", truck_number)
            # print("Batch", truck_number, "package count: ", batch_package_count)
            # if package_match_count == len(some_package_keys):
            #     print("\nTotal package count: ", total_package_count)

            Truck.trucks_dict.get(truck_number).load_truck(batch)

            batch.clear()
            address_associated_packages.clear()
            batch_package_count = 0
            can_load_more = True







