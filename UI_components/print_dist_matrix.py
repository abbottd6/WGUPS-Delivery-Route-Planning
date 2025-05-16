line_format = ''

def print_dist_matrix(some_distance_matrix, n):

    print_text = [f"\n{line_format:_<400}", "DESTINATION DISTANCE MATRIX",
                    f"{line_format:_<400}\n"]
    for i in range(n):
        row = some_distance_matrix[i]
        recipient = row[0]
        formatted = f"{recipient:<36} " + " ".join(f"{val:<28}" for val in row[1:])
        print_text.append(formatted)
    print_text.append(f"{line_format:_<400}\n")

    return "\n".join(print_text)