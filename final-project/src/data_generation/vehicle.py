from tenacity import abstractmethod


class Vehicle:
    @abstractmethod
    def consumption(self, speed: float) -> float:
        pass
    
    @abstractmethod
    def replenishment_time(self, current_resources: float) -> float:
        pass
