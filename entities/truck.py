from collections import deque


class Truck:
    trucks_dict = {}

    def __init__(self, truck_id, driver_id, current_location):
        self.truck_id = truck_id
        self.driver_id = driver_id
        self.packages = deque()
        self.current_location = current_location

        Truck.trucks_dict[truck_id] = self

    def __str__(self):
        truck_info = f"Truck #{self.truck_id}:"
        driver_info = f"Driver: {self.driver_id}"
        packages_str = "\n".join(str(p) for p in self.packages) if self.packages else "No packages loaded"
        line_format = ""
        return (f"\n{line_format:_<400}\n"
                f"Batch {self.truck_id} Loaded onto Truck with Optimized Route:"
                f"\n{line_format:_<400}\n"
                f"{truck_info:<4} {driver_info:<4}\n"
                f"Truck Location: {self.current_location}\n"
                f"{packages_str}\n"
                f"\n{line_format:_<400}\n")

    def load_truck(self, batch):
        while len(batch) > 0:
            self.packages.append(batch.popleft())