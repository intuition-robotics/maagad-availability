from abc import ABC, abstractmethod
from hri_framework.HRI_LIB.hri_interfaces.hri_request_handlers import HRIRequest


class Decision:
    # go            = true / false --> go / no go
    # speedFactor   = a value 0..2 affecting the speed of actions, i.e., speed --> speed*value
    # emotion       = a string depcting the emotion of the robot, may affect face displays or LLM messages
    # reason        = a string explaining the reason
    def __init__(self,go:bool, speedFactor:float, emotion:str, reason:str) -> None:
        self.go=go # go / no go
        self.speedFactor=speedFactor
        self.emotion=emotion
        self.reason=reason

class DecisionHelper(ABC):
    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def decide(self, req:HRIRequest) -> Decision: 
        pass