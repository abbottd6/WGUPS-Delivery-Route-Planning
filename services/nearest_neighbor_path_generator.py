from utils.calc_travel_time import calc_travel_time

line_format = ''

def nearest_neighbor_path_generator(some_package_keys, some_package_hash_table,
                                    some_distance_matrix):
    HUB_ADDRESS = some_distance_matrix[0][1]
    distance_traveled_array = []
    current_node_address = ''
    current_node_index = 0
    visited_nodes = []
    aggregate_time = 0.0
    destination_count = 0
    num_packages_delivered = 0


    #finding the starting node
    for i, row in enumerate(some_distance_matrix[1:], start=1):
        if row[1] == 0.0:
            current_node_address = row[0]
            visited_nodes.append(current_node_address)
            current_node_index = i
        destination_count = i

    # print("CURRENT NODE: ", current_node_address)
    # print("NEXT_NODE 'DISTANCE MATRIX' ROW INDEX:", current_node_index)
    # print("Package keys: ", len(some_package_keys))

    neighbor_distances_array = {}
    for delivery_stop in range(1, destination_count + 1):

        for row in some_distance_matrix[1:]:
            if not any(row[0] in node for node in visited_nodes):
                neighbor_distances_array[row[0]] = row[current_node_index]
            else:
                continue

        nearest_neighbor = min(neighbor_distances_array.items(), key=lambda item: item[1])

        for i, row in enumerate(some_distance_matrix[1:], start=1):
            if row[0] == nearest_neighbor[0]:
                current_node_index = i

        # print("NEXT PATH NODE AND DISTANCE:", nearest_neighbor)
        # print("NEXT_NODE 'DISTANCE MATRIX' ROW INDEX:", current_node_index)

        associated_packages = some_package_hash_table.get_by_address(nearest_neighbor[0])

        visited_nodes.append(associated_packages[0].address)
        # print(visited_nodes[0])

        path_time = calc_travel_time(nearest_neighbor[1])

        aggregate_time += path_time
        distance_traveled_array.append(nearest_neighbor[1])
        neighbor_distances_array[current_node_address] = nearest_neighbor[0]


        neighbor_distances_array.clear()

        num_packages_delivered += len(associated_packages)

        if num_packages_delivered >= len(some_package_keys):
            break

    nearest_neighbor_route = {}
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
        if d == len(visited_nodes) - 1:
            final_delivery_matrix_index = some_distance_matrix[0].index(route_info["address"])
            return_to_hub_distance = some_distance_matrix[final_delivery_matrix_index][1]

            route_termination_info = {
                "end_location": "HUB",
                "address": HUB_ADDRESS,
                "distance": return_to_hub_distance
            }

        nearest_neighbor_route[d] = route_info
        if d == len(visited_nodes) - 1:
            nearest_neighbor_route[d + 1] = route_termination_info


    return nearest_neighbor_route
