from services.package_data_parser import distance_matrix
from UI_components.print_dist_matrix import print_dist_matrix


def distance_matrix_builder(some_package_keys, some_package_hash_table):
    hub = distance_matrix[0][1]

    batch_destinations = [hub]

    # Add unique addresses to array of addresses for matrix population.
    for package_id in some_package_keys:
        temp_package = some_package_hash_table.get_by_id(package_id)
        for column in distance_matrix[0]:
            if column in temp_package.address and not column in batch_destinations:
                batch_destinations.append(column)

    # Create square matrix with dimensions equivalent to number of destinations + 1.
    n = len(batch_destinations) + 1
    temp_dist_matrix = [[0 for _ in range(n)] for _ in range(n)]

    # Populate first row and first column with addresses for distance associations.
    for i, destination in enumerate(batch_destinations, start=1):
        temp_dist_matrix[0][i] = destination
        temp_dist_matrix[i][0] = destination

    # Get distances from full distance matrix that correspond only to distances between
    # addresses in this distance matrix.
    # Insert the distances in to the matrix at the coordinates that correspond to the associated
    # addresses.
    for address in distance_matrix[0]:
        try:
            primary_index = batch_destinations.index(address) + 1
            parent_matrix_index = distance_matrix[0].index(address)
            for i, row_values in enumerate(distance_matrix[parent_matrix_index]):
                if distance_matrix[0][i] in batch_destinations:
                    secondary_index = batch_destinations.index(distance_matrix[0][i]) + 1
                    temp_dist_matrix[primary_index][secondary_index] = row_values
        except ValueError:
            continue

    print_dist_matrix(temp_dist_matrix, n)

    # Return this distance matrix for assignment where called.
    return temp_dist_matrix