from datetime import datetime

from entities.truck import Truck
from services.nearest_neighbor_path_generator import nearest_neighbor_path_generator
from services.package_priority_parsing_service import package_priority_parsing_service

def start_delivery_service(all_package_keys, all_package_hash_table, all_distance_matrix):

    route_objects = package_priority_parsing_service(all_package_keys, all_package_hash_table)

    for route in route_objects:
        print(route)

    for truck in Truck.trucks_dict.values():
        print(truck)