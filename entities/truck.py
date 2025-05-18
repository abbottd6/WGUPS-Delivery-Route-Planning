from collections import deque
from datetime import datetime

TIME_FORMAT = "%I:%M %p"

class Truck:
    trucks_dict = {}

    def __init__(self, truck_id, driver_id, route_start_time, en_route_time, status, distance_traveled):
        self.truck_id = truck_id
        self.driver_id = driver_id
        self.packages = deque()
        self.route_start_time = route_start_time
        self.en_route_time = en_route_time
        self.distance_traveled = distance_traveled

        self.status = status

        Truck.trucks_dict[truck_id] = self

    def __str__(self):
        truck_info = f"Truck #{self.truck_id}"
        driver_info = f"Driver ID: {self.driver_id}"
        packages_str = "\n".join(str(p) for p in self.packages) if self.packages else "No packages loaded"
        line_format = ""
        return (f"\n{line_format:_<400}\n"
                f"Batch #{self.truck_id} Loaded onto Truck for Optimized Route:"
                f"\n{line_format:_<400}\n"
                f"{truck_info:<4}\n"
                f"{driver_info:<4}\n"
                f"Departure Time: {datetime.strftime(self.route_start_time, TIME_FORMAT)}\n"
                f"Time on Route: {self.en_route_time} minutes\n"
                f"Truck Route Distance Traveled: {self.distance_traveled} miles\n"
                f"Truck Status: {self.status}\n\n"
                f"{packages_str}\n"
                f"\n{line_format:_<400}\n")

    def load_truck(self, batch):
        while len(batch) > 0:
            self.packages.append(batch.popleft())