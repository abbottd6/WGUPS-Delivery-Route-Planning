from services.package_data_parser import num_destinations, distance_matrix
from services.package_data_parser import package_hash_table
from services.package_data_parser import package_keys

line_format = ''

def delivery_route_generator():

    distance_traveled = []
    current_node = 1
    next_node = 0
    visited_nodes = []
    packages_delivered = 0
    path_time = 0
    aggregate_time = 0
    truck_speed = 18


    #finding the starting node
    for i, row in enumerate(distance_matrix[1:], start=1):
        if row[1] == 0.0:
            current_node = row[0]
            visited_nodes.append(current_node)
            next_node = i

    # print("CURRENT NODE: ", current_node)
    # print("NEXT NODE: ", next_node)

    for delivery_stop in range(len(package_keys)):
        dist_options = {}

        for row in distance_matrix[1:]:
            if (row[next_node] != 0.0) and (row[next_node] != 'X') and (row[0] not in visited_nodes):
                dist_options[row[0]] = row[next_node]
            else:
                continue

        path_node = min(dist_options.items(), key=lambda item: item[1])

        for i, row in enumerate(distance_matrix[1:], start=1):
            if row[0] == path_node[0]:
                next_node = i

        # print("PATH NODE:", path_node)
        #
        # print("NEXT NODE:", next_node)

        associated_packages = package_hash_table.get_by_address(path_node[0])
        packages_delivered += len(associated_packages)
        # for i, package in enumerate(associated_packages, start=1):
        #     print("Associated Package", i, ":", package)
        # for row in associated_packages:
        #     print(row)

        visited_nodes.append(associated_packages[0].address)
        # print(visited_nodes[0])

        path_time = path_node[1] * (60 / truck_speed)
        print("Delivery #", delivery_stop, ": required", path_node[1],
              "miles of travel and was completed in", path_time, "minutes.")
        aggregate_time += path_time
        distance_traveled.append(path_node[1])
        dist_options[current_node] = path_node[0]

        dist_options.clear()

        if packages_delivered >= len(package_keys):
            total_distance = sum(distance_traveled)

            print(f"\n{line_format:_<200}\n")
            print("ALL PACKAGES DELIVERED\n")
            print("Total Distance Traveled: ", total_distance, "\n")
            print("Locations visited: ", len(visited_nodes))
            print("Elapsed Time: ", aggregate_time, "\n")
            print(f"\n{line_format:_<200}\n")
            break

        # print(path_node)
        # print(dist_options)


