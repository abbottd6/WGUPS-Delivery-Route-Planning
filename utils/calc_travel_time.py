TRUCK_SPEED = 18

def calc_travel_time(distance):
    path_time = distance * (60 / TRUCK_SPEED)
    return path_time