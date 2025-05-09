# Package class to instantiate package objects with attributes corresponding
# to those provided in the Package File Excel doc
class Package:
    def __init__(self, package_id, address, city, state, zip_code,
                 deadline, weight, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At Hub"

    # method for stringifying a Package object and adding min fields widths
    # for improved readability
    def __str__(self):
        package_label = f"Package {self.package_id}:"
        return (f"{package_label:<14} {self.status:<10} {self.address:50} "
                f"{self.city:20} {self.state:8} {self.zip_code:8} "
                f"{self.deadline:10} {self.weight:8}kg {self.notes:^65}")

    # method used in the custom_hash_table insert method to concat a duplicate
    # message to the package's note if the package ID has a duplicate attempt
    # to insert it into the hash table
    def append_note(self, new_note):
        if self.notes:
            self.notes = self.notes + "; " + new_note
