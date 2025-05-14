from services.package_data_parser import distance_matrix
from UI_components.print_dist_matrix import print_dist_matrix


def distance_matrix_builder(some_package_keys, some_package_hash_table):
    hub = distance_matrix[0][1]

    batch_destinations = [hub]

    for package_id in some_package_keys:
        temp_package = some_package_hash_table.get_by_id(package_id)
        # print(package_id)
        # print(temp_package)
        for column in distance_matrix[0]:
            if column in temp_package.address and not column in batch_destinations:
                batch_destinations.append(column)

    n = len(batch_destinations) + 1
    temp_dist_matrix = [[0 for _ in range(n)] for _ in range(n)]

    for i, destination in enumerate(batch_destinations, start=1):
        temp_dist_matrix[0][i] = destination
        temp_dist_matrix[i][0] = destination

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

    return temp_dist_matrix