line_format = ""

def print_route_distances(route, num_destinations):
    print_text = [f"{line_format:_<400}\n",
                  "DELIVERY NUMBER       |              ADDRESS              |       DISTANCE "
                  "FROM PREVIOUS", f"{line_format:_<400}\n"
                  ]
    for i in range(num_destinations):
        values = route[i]
        address = values.get("address")
        distance = values.get("distance")
        print_text.append(f"{i:<21} {address:^35} {distance:>29}\n")
    print_text.append(f"{line_format:_<400}\n")
    return "\n".join(print_text)