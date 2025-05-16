from UI_components.print_all_packages import print_all_packages
from UI_components.print_dist_matrix import print_dist_matrix
from UI_components.print_route_metadata import print_route_metadata

line_format = ""

class Route:
    def __init__(self, route_label=None, route_package_keys=None, route_package_table=None, route_num_destinations=None,
                 route_distance_matrix=None, route=None):
        self.route_label = route_label
        self.route_package_keys = route_package_keys
        self.route_package_table = route_package_table
        self.route_num_destinations = route_num_destinations
        self.route_distance_matrix = route_distance_matrix
        self.route = route

    def __str__(self):
        package_table = print_all_packages(self.route_package_keys, self.route_package_table, self.route_label)
        num_destinations = len(self.route_distance_matrix[0])
        return (f"{line_format:_<400}\n \n{package_table}\n"
                f"{print_dist_matrix(self.route_distance_matrix, num_destinations)}"
                f"{print_route_metadata(self.route, self.route_num_destinations)}\n")