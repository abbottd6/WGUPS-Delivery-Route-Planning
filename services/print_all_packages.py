import time

line_format = ""

def print_all_packages(keys_array, some_hash_table, label):
    print(f"{line_format:_<200}\n")
    print("Currently Tracking", label, ":")
    print(f"{line_format:_<200}\n")
    for package_id in keys_array:
        print(some_hash_table.get_by_id(package_id))
        time.sleep(0.025)
    print(f"\n{line_format:_<200}\n")