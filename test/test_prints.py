from services import package_data_parser
from entities import package
from services.package_data_parser import package_hash_table
from services.package_data_parser import package_keys

# Printing all rows from the csv file
for row in package_data_parser.package_data:
    print(row)

# verifying the correct number of packages have been inserted into package_hash_table
if (len(package_keys) == 40) and (package_hash_table.count == 40):
    # test print to check hash table creation and population from csv file
    print("\n \n Packages successfully transferred to hash table: \n")
    for package_id in package_keys:
        print(package_hash_table.get_by_id(package_id))

# testing append_note method for adding note about duplicate id's if key already exists
# during insert into hash table
test_package = package.Package(38, '410 S State St', 'Salt Lake City', 'UT',
                               '84111', 'EOD', '9', 'Can only be on truck 2')
package_hash_table.insert(test_package.package_id, test_package)

print(package_hash_table.get_by_id(test_package.package_id))