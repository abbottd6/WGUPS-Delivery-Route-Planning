from services.package_data_parser import num_destinations, distance_matrix

line_format = ''

def print_dist_matrix():
    print(f"\n{line_format:_<200}\n")
    print("RECIPIENT DISTANCE MATRIX")
    print(f"{line_format:_<200}\n")
    for i in range(num_destinations):
        row = distance_matrix[i]
        recipient = row[0]
        formatted = f"{recipient:<45} " + " ".join(f"{val:<8}" for val in row[1:])
        print(formatted)
    print(f"\n{line_format:_<200}\n")