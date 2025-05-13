from entities.driver import Driver
from entities.truck import Truck
from services.package_data_parser import package_hash_table, package_keys
from collections import deque

from utils.instantiate_delivery_infra import instantiate_delivery_infra


def delivery_batch_builder(route_path):
    total_package_count = 0
    batch = deque()
    truck_number = 1
    batch_package_count = 0
    package_match_count = 0
    carryover_packages = []

    for delivery_stop in route_path.values():
        if carryover_packages:
            for carryover_package in carryover_packages:
                batch.append(carryover_package)
                batch_package_count += 1
                total_package_count += 1
            carryover_packages = []

        address_associated_packages = package_hash_table.get_by_address(delivery_stop["address"])
        package_match_count += len(address_associated_packages)

        if len(address_associated_packages) == 0:
            continue
        if (batch_package_count + len(address_associated_packages) <= 16) and total_package_count < len(package_keys):
            for package in address_associated_packages:
                    batch.append(package_hash_table.get_by_id(package.package_id))
                    batch_package_count += 1
                    total_package_count += 1
            can_load_more = True
        else:
            can_load_more = False
            for package in address_associated_packages:
                carryover_packages.append(package_hash_table.get_by_id(package.package_id))
        if (batch_package_count == 16) or (package_match_count == len(package_keys)) or can_load_more == False:

            # print("\nTruck number: ", truck_number)
            # print("Batch", truck_number, "package count: ", batch_package_count)
            # if package_match_count == len(package_keys):
            #     print("\nTotal package count: ", total_package_count)

            Truck.trucks_dict.get(truck_number).load_truck(batch)

            batch.clear()
            address_associated_packages.clear()
            batch_package_count = 0
            truck_number += 1
            can_load_more = True
    # print(Truck.trucks_dict.get(truck_number).packages)
    for truck in Truck.trucks_dict.values():
        print(truck)






