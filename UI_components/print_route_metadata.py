from UI_components.print_all_packages import print_all_packages

line_format = ""

def print_route_metadata(route, num_destinations):
    print_text = [f"{line_format:_<400}\n",
                  "DELIVERY NUMBER       |              ADDRESS              |       DISTANCE "
                  "FROM PREVIOUS       |       ASSOCIATED PACKAGE ID's", f"{line_format:_<400}\n"
                  ]
    for key in sorted(route):
        values = route[key]
        address = values.get("address")
        distance = values.get("distance")
        associated_packages = values.get("associated_packages")
        if associated_packages is None:
            package_strs = "None"
        else:
            package_strs = ", ".join(str(p.package_id) for p in values["associated_packages"])
        print_text.append(f"{key:<21} {address:^35} {distance:^40} {package_strs:^30}")
    print_text.append(f"{line_format:_<400}\n")
    return "\n".join(print_text)