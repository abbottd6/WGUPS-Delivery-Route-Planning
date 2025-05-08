import csv
from resources import *
from utils.custom_hash_table import PackageHashTable
from entities.package import Package

# Reading package data from csv into lists
with open ('../resources/WGUPS Package File.csv') as csvfile:
    package_data = list(csv.reader(csvfile, delimiter=','))

# Reading package distance table into lists
with open ('../resources/WGUPS Distance Table.csv') as csvfile:
    distance_table = list(csv.reader(csvfile, delimiter=','))

# Creating a list comprising the individual rows (i.e., packages) from csv.
# The list excludes rows/arrays that do not begin with a digit;
# this gets rid of header rows from the csv that are not packages
package_rows = [row for row in package_data[0:] if row[0].strip().isdigit()]

# Creating hash table using custom PackageHashTable class and _next_prime method
# to create a table that is of size (num packages in csv * 2) ++ to next prime)).
package_hash_table = PackageHashTable(len(package_rows))

# Creating a list of package keys for testing the package_hash_table population.
package_keys = []

# Looping through each row array and extracting data by array index position
# to assign it to the corresponding package attribute.
# Also, adding each package_id to package_keys so that I can test that the hash table
# has populated correctly later (it's in test_prints.py).
for row in package_rows:
    package_id = int(row[0])
    package_keys.append(package_id)
    address = row[1]
    city = row[2]
    state = row[3]
    zip_code = row[4]
    deadline = row[5]
    weight = float(row[6])
    notes = row[7]

# Creating a temp package from the attributes assigned in each row...
    temp_package = Package(package_id, address, city, state, zip_code, deadline, weight, notes)

# so that the temp package can be inserted into the package_hash_table
    package_hash_table.insert(package_id, temp_package)
