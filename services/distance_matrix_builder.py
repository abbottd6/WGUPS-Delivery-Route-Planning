from services.package_data_parser import distance_matrix
from services.print_dist_matrix import print_dist_matrix


def distance_matrix_builder(some_package_keys, some_package_hash_table):
    batch_destinations = []

    for package_id in some_package_keys:
        temp_package = some_package_hash_table.get_by_id(package_id)
        print(package_id)
        print(temp_package)
        for column in distance_matrix[0]:
            if column in temp_package.address:
                batch_destinations.append(column)

    n = len(batch_destinations)
    temp_dist_matrix = [[0 for _ in range(n)] for _ in range(n)]

    # INSERT THE ADDRESS AND DISTANCE VALUES FROM PRIMARY MATRIX INTO TEMP MATRIX

    print_dist_matrix(temp_dist_matrix, n)

    # RETURN TEMP MATRIX