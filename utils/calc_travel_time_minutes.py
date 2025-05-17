TRUCK_SPEED = 18

def calc_travel_time_minutes(distance):
    path_time_minutes = (distance / TRUCK_SPEED) * 60
    return path_time_minutes