line_format = ''

def print_dist_matrix(some_distance_matrix, n):
    print(f"\n{line_format:_<200}\n")
    print("RECIPIENT DISTANCE MATRIX")
    print(f"{line_format:_<200}\n")
    for i in range(n):
        row = some_distance_matrix[i]
        recipient = row[0]
        formatted = f"{recipient:<36} " + " ".join(f"{val:<28}" for val in row[1:])
        print(formatted)
    print(f"\n{line_format:_<200}\n")