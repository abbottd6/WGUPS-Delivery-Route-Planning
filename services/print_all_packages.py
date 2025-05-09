import time
from services.package_data_parser import package_hash_table
from services.package_data_parser import package_keys

line_format = ""

def print_all_packages():
    print(f"{line_format:_<200}\n")
    print("Currently Tracked Packages:")
    print(f"{line_format:_<200}\n")
    for package_id in package_keys:
        print(package_hash_table.get_by_id(package_id))
        time.sleep(0.025)
    print(f"\n{line_format:_<200}\n")