from abc import ABC


availabilityState=dict()

class AvailabilityManager(ABC):


    @staticmethod
    def set_availability(user:str, available:bool):
        availabilityState[user]=available


    @staticmethod
    def is_available(user:str) -> bool:
        return availabilityState[user] if user in availabilityState else False
