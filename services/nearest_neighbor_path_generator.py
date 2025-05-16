from utils.calc_travel_time import calc_travel_time
from datetime import datetime

time_format = "%I:%M %p"
line_format = ''

def nearest_neighbor_path_generator(some_package_keys, some_package_hash_table,
                                    some_distance_matrix):
    HUB_ADDRESS = some_distance_matrix[0][1]
    distance_traveled_array = []
    current_node_address = ''
    current_node_index = 0
    visited_nodes = []
    high_priority_packages = []
    high_priority_package_keys = []
    aggregate_time = 0.0
    destination_count = 0
    num_packages_delivered = 0

    # Isolate packages with specified delivery time deadlines into a separate array.
    deadline_package_keys = []
    for package_key in some_package_keys:
        if "EOD" not in some_package_hash_table.get_by_id(package_key).deadline:
            deadline_package_keys.append(package_key)

    # Loop to compare package deadline with the deadlines of other packages.
    for package_key in deadline_package_keys:
        package_to_check = some_package_hash_table.get_by_id(package_key)
        if "EOD" in package_to_check.deadline:
            continue
        # Convert given time string to a datetime object of format HH:MM AM/PM.
        this_deadline = datetime.strptime(package_to_check.deadline, time_format).time()
        # If this_deadline is less than any other deadline (i.e., deadline is sooner), then the package has priority.
        if any(
                this_deadline < (datetime.strptime(some_package_hash_table.get_by_id(other_key).deadline,
                    time_format).time())
                for other_key in deadline_package_keys
        ):
            # If the package has priority, then add it to the high_priority_packages array and the key array.
            high_priority_packages.append(package_to_check)
            high_priority_package_keys.append(package_key)

    # Find the starting node i.e., the hub.
    for i, row in enumerate(some_distance_matrix[1:], start=1):
        if row[1] == 0.0:
            current_node_address = row[0]
            visited_nodes.append(current_node_address)
            current_node_index = i
        destination_count = i

    # Check if there are any packages in high priority package array for this batch.
    if high_priority_packages:
        # For all packages in the high_priority_packages_array (identified by keys array).
        for package_key in high_priority_package_keys:
            # Get package delivery address from hash table.
            this_address = some_package_hash_table.get_by_id(package_key).address
            # Get all other address associated packages.
            associated_packages = some_package_hash_table.get_by_address(
                some_package_hash_table.get_by_id(package_key).address)
            # Add the high_priority package address to visited nodes.
            visited_nodes.append(associated_packages[0].address)

            # Get the distance matrix index position for this address.
            for i, address in enumerate(some_distance_matrix[0][1:], start=1):
                if this_address in address:
                    this_address_index = i
                    # break from loop when found
                    break
            # Get the distance from the current address (e.g., the hub) to this high priority delivery address
            # and append it to the distance traveled array.
            distance_traveled_array.append(some_distance_matrix[this_address_index][current_node_index])
            # Set current_node_index and current_node_address for next loop iteration
            current_node_index = this_address_index
            current_node_address = this_address

            # Increment the number of packages delivered by the number of packages associated with this address
            num_packages_delivered += len(associated_packages)

        # Clear the list so that the next loop iteration can skip this block
        # because there are no more priority packages
        high_priority_packages.clear()


    if not high_priority_packages:
        # Create an empty dictionary to hold the distances TO other destinations FROM current_node.
        neighbor_distances_array = {}
        for delivery_stop in range(len(high_priority_package_keys), destination_count + 1):
            # Add each neighbor distance for current_node to the distance dictionary.
            for row in some_distance_matrix[1:]:
                # First, check that the distance being added does not correspond to an already visited
                # destination.
                if not any(row[0] in node for node in visited_nodes):
                    # If the distance value does not correspond to a visited node, add it to distance
                    # dictionary, where the key is the node address and the value is the distance to
                    # that node from current_node.
                    neighbor_distances_array[row[0]] = row[current_node_index]
                else:
                    continue

            # Identify the nearest neighbor to be the dictionary element containing the smallest
            # distance value.
            nearest_neighbor = min(neighbor_distances_array.items(), key=lambda item: item[1])

            # Adjust current_node_index to be this nearest_neighbor in prep for next iteration.
            for i, row in enumerate(some_distance_matrix[1:], start=1):
                if row[0] == nearest_neighbor[0]:
                    current_node_index = i

            # Gather packages associated with the address of nearest_neighbor into a hash table.
            associated_packages = some_package_hash_table.get_by_address(nearest_neighbor[0])

            # Add associated_packages address to visited nodes if there are packages associated with
            # this address.
            visited_nodes.append(associated_packages[0].address)
            # print(visited_nodes[0])

            path_time = calc_travel_time(nearest_neighbor[1])

            aggregate_time += path_time
            distance_traveled_array.append(nearest_neighbor[1])
            neighbor_distances_array[current_node_address] = nearest_neighbor[0]

            # Empty reusable data structure for next iteration.
            neighbor_distances_array.clear()

            # Aggregate the total number of packages delivered in this route for
            # termination upon delivery of all packages.
            num_packages_delivered += len(associated_packages)

            # Terminate route planning if all packages have been accounted for.
            if num_packages_delivered >= len(some_package_keys):
                break

    # Create a dictionary to insert optimized route based on delivery sequence value (as key).
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
        # Calculate return to hub distance from final delivery address.
        if d == len(visited_nodes) - 1:
            final_delivery_matrix_index = some_distance_matrix[0].index(route_info["address"])
            return_to_hub_distance = some_distance_matrix[final_delivery_matrix_index][1]

            route_termination_info = {
                "end_location": "HUB",
                "address": HUB_ADDRESS,
                "distance": return_to_hub_distance
            }
        # Add dictionary value for each destination to route dictionary.
        nearest_neighbor_route[d] = route_info

        # Add return to HUB to delivery route if all deliveries for route are complete.
        if d == len(visited_nodes) - 1:
            nearest_neighbor_route[d + 1] = route_termination_info

    # Return the route dictionary for assignment where called.
    return nearest_neighbor_route
