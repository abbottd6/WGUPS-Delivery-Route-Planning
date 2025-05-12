import csv
from utils.custom_hash_table import PackageHashTable
from entities.package import Package

# Reading package data from csv into lists
with open ('./resources/WGUPS Package File.csv') as csvfile:
    package_data = list(csv.reader(csvfile, delimiter=','))

# Reading package distance table into lists
with open ('./resources/WGUPS Distance Table.csv') as csvfile:
    distance_table = list(csv.reader(csvfile, delimiter=','))

# Creating a list comprising the individual rows (i.e., packages) from csv.
# The list excludes rows/arrays that do not begin with a digit;
# this gets rid of header rows from the csv that are not packages
package_rows = [row for row in package_data[0:] if row[0].strip().isdigit()]

# Extracting only the rows that represent recipients from the distance table
# and placing them in an array for mapping to the matrix.
distance_table_rows = []
for row in distance_table[0:]:
    try:
        # if the value at index position 2 (distance from hub) of the row cannot be converted to a float
        # then the row is not a recipient row and should not be included in the recipient count
        float(row[2])

        # Adding each recipient row to the distance_table_rows to reconstruct the recipient
        # table, but with only the rows representing recipients
        distance_table_rows.append(row)

    # catching errors from the attempt to convert to float from above and continuing, i.e. skipping
    # that row if float conversion throws an error
    except(ValueError, TypeError):
        continue


# creating a variable that holds the number of recipients + 1 for defining matrix size
# the + 1 is required because there is one additional row and column required for the
# recipient names/identifiers
num_destinations = len(distance_table_rows) + 1


# Creating hash table using custom PackageHashTable class and _next_prime method
# to create a table that is of size (num packages in csv * 2) ++ to next prime)).
package_hash_table = PackageHashTable(len(package_rows))

distance_matrix = [[0 for _ in range(num_destinations)] for _ in range(num_destinations)]


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

# Constructing a two-dimensional array/matrix from the distance table csv.
index = 1
distance_matrix[0][0] = 'RECIPIENT'
for row in distance_table_rows:

    # Parsing address/recipient/zipcode identifiers from csv rows and extracting the recipient name
    recipient = row[0].split('\n')
    recipient = recipient[1].strip()
    recipient = recipient.strip(',')

    # Extracting initial letters of recipient info to generate a string abbreviation for the recipient
    # name to make the top row of the matrix readable and allow column values to line up visually with
    # their corresponding distance values
    recipient_abrev = recipient[0:24]

    # Inserting abbreviated recipient names in corresponding top row index positions
    distance_matrix[0][index] = recipient_abrev

    # Inserting non-abbreviated recipient names along the corresponding rows in index 0
    distance_matrix[index][0] = recipient_abrev

    # Mapping distance values from the csv to the correct location within the matrix
    for col in range(1, num_destinations):
        # If the value cannot be converted to a float, then it is not a distance value.
        # So, I use a try/catch block to try to convert each value to a float.
        try:
            distance_matrix[index][col] = 'X'
            # If this throws an error, then the value is not a distance value and retains
            # a placeholder "X" for improved readability.
            dist = float(row[col + 1])

            # if the value can be converted to a float, then it is added to the matrix in the position
            # that corresponds to its distance between two locations
            distance_matrix[index][col] = dist
            distance_matrix[col][index] = dist

        # Catching errors from the attempt to convert to float from above and continuing i.e., skipping
        # that element if float conversion throws an error.
        # The try block sets every index value to X before attempting the float conversion, so
        # if the value fails the float conversion it retains the placeholder X
        except(ValueError, TypeError):
            continue

    index += 1


