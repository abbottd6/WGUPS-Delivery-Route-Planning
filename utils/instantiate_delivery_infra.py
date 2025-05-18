from entities.driver import Driver
from entities.truck import Truck


def instantiate_delivery_infra():

    truck1 = Truck(truck_id=1, driver_id =None, status = "At Hub", route_start_time="08:00 AM", en_route_time=0,
                   distance_traveled=0)
    truck2 = Truck(truck_id=2, driver_id=None, status="At Hub", route_start_time="09:05 AM", en_route_time=0,
                   distance_traveled=0)
    truck3 = Truck(truck_id=3, driver_id=None, status="At Hub", route_start_time=None, en_route_time=0,
                   distance_traveled=0)

    driver1 = Driver(driver_id=1, assigned_truck = None, status = "Open")
    driver2 = Driver(driver_id=2, assigned_truck = None, status = "Open")