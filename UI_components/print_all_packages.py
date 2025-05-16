import time

line_format = ""

def print_all_packages(keys_array, some_hash_table, label):
    print_text = [f"\n{line_format:_<400}\n", "Currently Tracking ", label, ":",
                  f"\n\nPackage Keys:{keys_array}"
                  f"\n{line_format:_<400}\n"]
    for package_id in keys_array:
        print_text.append(f"{some_hash_table.get_by_id(package_id)}\n")
    print_text.append(f"{line_format:_<400}\n")
    return "".join(print_text)