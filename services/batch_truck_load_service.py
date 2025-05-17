from entities.truck import Truck
from collections import deque

def batch_truck_load_service(route_path, some_package_keys, some_package_hash_table, label):
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
        # Check whether there are carryover_packages from last batch; see ---->>>> below.
        # If carryover packages exist, add them to current batch.
        if carryover_packages:
            for carryover_package in carryover_packages:
                batch.append(carryover_package)
                batch_package_count += 1
                total_package_count += 1
            carryover_packages = []

        # Check hash table for other packages associated with this address so that they can be
        # delivered at the same time
        address_associated_packages = some_package_hash_table.get_by_address(delivery_stop["address"])
        package_match_count += len(address_associated_packages)

        # If there are no associated_packages (e.g., it is the hub)
        # then don't load packages for this address. Continue to loop condition.
        if len(address_associated_packages) == 0:
            continue

        # Compare what the size of the batch would be if associated_packages were added to the batch.
        # Do not attempt to load if batch size would be above truck capacity.
        if (batch_package_count + len(address_associated_packages) <= 16) and total_package_count < len(some_package_keys):
            for package in address_associated_packages:
                    batch.append(some_package_hash_table.get_by_id(package.package_id))
                    batch_package_count += 1
                    total_package_count += 1
            can_load_more = True
        else:
            can_load_more = False
            # ---->>>>
            # If this point is reached, then the number of associated_packages is too large to fit in
            # the current truck batch. But the loop iteration has already visited this address, so
            # we cannot just continue the loop or these packages will be skipped for truck loading.
            # Add the associated packages to carry_over_packages for inclusion in the next batch.
            for package in address_associated_packages:
                carryover_packages.append(some_package_hash_table.get_by_id(package.package_id))

        # Once the number of packages in a batch reaches the maximum possible per constraints,
        # load the packages onto corresponding truck and clear batch to start new.
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







