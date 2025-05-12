from services.package_data_parser import num_destinations, distance_matrix
from services.package_data_parser import package_hash_table
from services.package_data_parser import package_keys
from utils.calc_travel_time import calc_travel_time

line_format = ''

def nearest_neighbor_path_generator():

    distance_traveled_array = []
    current_node_address = ''
    current_node_index = 0
    visited_nodes = []
    packages_delivered_count = 0
    aggregate_time = 0.0
    destination_count = 0
    num_packages_delivered = 0


    #finding the starting node
    for i, row in enumerate(distance_matrix[1:], start=1):
        if row[1] == 0.0:
            current_node_address = row[0]
            visited_nodes.append(current_node_address)
            current_node_index = i
        destination_count = i

    # print("CURRENT NODE: ", current_node_address)
    # print("NEXT_NODE 'DISTANCE MATRIX' ROW INDEX:", current_node_index)
    # print("Package keys: ", len(package_keys))

    neighbor_distances_array = {}
    for delivery_stop in range(1, destination_count + 1):

        for row in distance_matrix[1:]:
            if not any(row[0] in node for node in visited_nodes):
                neighbor_distances_array[row[0]] = row[current_node_index]
            else:
                continue

        nearest_neighbor = min(neighbor_distances_array.items(), key=lambda item: item[1])

        for i, row in enumerate(distance_matrix[1:], start=1):
            if row[0] == nearest_neighbor[0]:
                current_node_index = i

        # print("NEXT PATH NODE AND DISTANCE:", nearest_neighbor)
        # print("NEXT_NODE 'DISTANCE MATRIX' ROW INDEX:", current_node_index)

        associated_packages = package_hash_table.get_by_address(nearest_neighbor[0])
        # for i, package in enumerate(associated_packages, start=1):
        #     num_packages_delivered += 1
        #     print("Associated Package", i, ":\n", package)

        # for row in associated_packages:
        #     print(row)

        visited_nodes.append(associated_packages[0].address)
        # print(visited_nodes[0])

        path_time = calc_travel_time(nearest_neighbor[1])
        # print("Delivery #", delivery_stop, ": required", nearest_neighbor[1],
        #         "miles of travel, included", len(associated_packages), "packages, "
        #         "and was completed in", path_time, "minutes. \n")
        # print(f"\n{line_format:_<200}\n")

        aggregate_time += path_time
        distance_traveled_array.append(nearest_neighbor[1])
        neighbor_distances_array[current_node_address] = nearest_neighbor[0]


        neighbor_distances_array.clear()

        num_packages_delivered += len(associated_packages)

        if num_packages_delivered >= len(package_keys):

            print(f"\n{line_format:_<200}\n")
            print("ALL PACKAGES DELIVERED\n")
            print("Locations visited: ", len(visited_nodes))
            print("Number of packages delivered:", num_packages_delivered)
            print("Total distance between deliveries:", sum(distance_traveled_array))
            print("Elapsed Time: ", aggregate_time, "\n")
            print(f"\n{line_format:_<200}\n")
            print("Visited nodes length: ", len(visited_nodes))
            print("Distance traveled array length: ", len(distance_traveled_array))
            break

    nearest_neighbor_route = [None] * len(visited_nodes)
    for d, destination in enumerate(visited_nodes):
        if d == 0:
            route_info = {
                "start_location": "HUB",
                "address": visited_nodes[0],
                "distance": 0
            }
        else:
            route_info = {
                "delivery_number": d,
                "address": visited_nodes[d],
                "distance": distance_traveled_array[d - 1]
            }
        nearest_neighbor_route[d] = route_info
    return nearest_neighbor_route
