from .vehicle import Vehicle

def gasoline_consumption(speed):
    if speed > 50:
        return 5 + 3e-4*(speed-50)**2

    return 5 + 3e-3*(speed-50)**2

def gasoline_refill_time(max_tank_capacity, current_tank_capacity):
    return 1 + (max_tank_capacity-current_tank_capacity) / 30

class GasolineVehicle(Vehicle):
    def __init__(self, tank_capacity: float):
        self.tank_capacity = tank_capacity

    def consumption(self, speed: float) -> float:
        return gasoline_consumption(speed)
    
    def replenishment_time(self, current_resources: float) -> float:
        return gasoline_refill_time(self.tank_capacity, current_resources)
