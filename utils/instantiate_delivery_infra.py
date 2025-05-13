from entities.driver import Driver
from entities.truck import Truck


def instantiate_delivery_infra():

    truck1 = Truck(truck_id=1, driver_id =None, current_location = "Hub")
    truck2 = Truck(truck_id=2, driver_id=None, current_location="Hub")
    truck3 = Truck(truck_id=3, driver_id=None, current_location="Hub")

    driver1 = Driver(driver_id=1, assigned_truck = None, status = "Open")
    driver2 = Driver(driver_id=2, assigned_truck = None, status = "Open")