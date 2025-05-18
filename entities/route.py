from UI_components.print_all_packages import print_all_packages
from UI_components.print_dist_matrix import print_dist_matrix
from UI_components.print_route_metadata import print_route_metadata

line_format = ""

class Route:
    def __init__(self, label=None, package_keys=None, package_table=None, num_destinations=None,
                 distance_matrix=None, metadata=None, total_distance=None, duration=None):
        self.label = label
        self.package_keys = package_keys
        self.package_table = package_table
        self.num_destinations = num_destinations
        self.distance_matrix = distance_matrix
        self.metadata = metadata
        self.total_distance = total_distance
        self.duration = duration

    def __str__(self):
        package_table = print_all_packages(self.package_keys, self.package_table, self.label)
        num_destinations = len(self.distance_matrix[0])
        return (f"{line_format:_<400}\n \n{package_table}\n"
                f"{print_dist_matrix(self.distance_matrix, num_destinations)}"
                f"\n\n"
                f"{line_format:_<400}"
                f"\n"
                f"NEAREST NEIGHBOR OPTIMIZED ROUTE DESTINATION DETAILS"
                f"\n"
                f"{print_route_metadata(self.metadata, self.num_destinations)}\n"
                f"Route Distance Total: {self.total_distance} miles\n"
                f"Route Duration: {self.duration} minutes\n")