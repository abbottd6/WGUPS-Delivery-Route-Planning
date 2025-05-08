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

    def __str__(self):
        return (f"Package {self.package_id}: {self.address}, "
                f"{self.city}, {self.state}, {self.zip_code}, "
                f"{self.deadline}, {self.weight}, {self.notes}")

    def append_note(self, new_note):
        if self.notes:
            self.notes = self.notes + "; " + new_note
