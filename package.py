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

    # method for stringifying a Package object for readability
    def __str__(self):
        return (f"Package {self.package_id}: {self.address}, "
                f"{self.city}, {self.state}, {self.zip_code}, "
                f"{self.deadline}, {self.weight}, {self.notes}")

    # method used in the custom_hash_table insert method to concat a duplicate
    # message to the package's note if the package ID has a duplicate attempt
    # to insert it into the hash table
    def append_note(self, new_note):
        if self.notes:
            self.notes = self.notes + "; " + new_note
