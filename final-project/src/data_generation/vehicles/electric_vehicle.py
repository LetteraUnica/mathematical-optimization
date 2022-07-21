from .vehicle import Vehicle

def ev_consumption(speed):
    if speed > 10:
        return 5 + 2e-4*(speed-10)**2

    return 5 + 3e-2*(speed-10)**2

def ev_refill_time(max_tank_capacity, current_tank_capacity):
    return 1 + (max_tank_capacity - current_tank_capacity) / 15 * 60

class ElectricVehicle(Vehicle):
    def __init__(self, battery_capacity: float):
        self.battery_capacity = battery_capacity

    def consumption(self, speed: float) -> float:
        return ev_consumption(speed)
    
    def replenishment_time(self, current_resources: float) -> float:
        return ev_refill_time(self.battery_capacity, current_resources)
