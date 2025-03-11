import math
from ament_index_python.packages import get_package_share_directory

from hri_framework.HRI_LIB.hri_interfaces.hri_request_handlers import HRIRequest,HRIResponse, HRIBeliefSystem
from hri_framework.HRI_LIB.hri_types.hri_action import HRIAction

from hri_framework.Context_Management.HRI_DB import HRI_DB

from hri_framework.HRI_LIB.hri_interfaces.llm import LLM


from abc import ABC, abstractmethod
import re
import json
import os
import importlib
import string


msgGen=True

tempSymbolTable=dict()

class EventHandler(ABC):

    def __init__(self) -> None:
        self.values=dict()
        #self.futures=dict()
        self.match=False
        self.ack=None
        self.onf=None
        self.ons=None
        self.socialPlanner=None
        self.person=None
        self.emotion="natural"
        self.id=0
        self.handled = False  # Add this flag
    
    def copy(self):
        n=type(self)()
        n.values=self.values.copy()
        #n.futures=self.futures.copy()
        n.match=self.match

        n.ack=self.ack.copy() if self.ack!=None else None
        n.onf=self.onf.copy() if self.onf!=None else None
        n.ons=self.ons.copy() if self.ons!=None else None
        n.socialPlanner= self.socialPlanner.copy() if self.socialPlanner!=None else None        
        n.person=self.person
        n.emotion=self.emotion
        return n

                

    def setValues(self,values):
        global tempSymbolTable
        for k,v in values.items():
            tempSymbolTable[k]=v

        if self.values==None or len(self.values)==0:
            self.values=values
        # else:
        #     print("self...")
        #     self.updateParameters()

        # self.updateSubHandlers()

    # def updateSubHandlers(self):
    #     print("ack...")
    #     self.updateHandler(self.ack)        
    #     print("on success...")
    #     self.updateHandler(self.ons)
    #     print("on failure...")
    #     self.updateHandler(self.onf)

    # def updateHandler(self,handler):
    #     if handler!=None:
    #         handler.updateParameters()
    #         handler.person=self.person
    
    def updateParameters(self):
        global tempSymbolTable
        futures=tempSymbolTable
        # for k,v in futures.items():
        #     self.values[k]=v

        print(f"\tsymtable {futures}")
        print(f"\tbefore values {self.values}")
        for k,v in self.values.items():
            if v in futures.keys():
                self.values[k]=futures[v]
            else:
                text=v
                # Define punctuation to strip (exclude { and })
                punctuation_to_strip = string.punctuation.replace("{", "").replace("}", "")
                # Replace words in the text based on futures
                text = ' '.join([
                    futures[w.strip(punctuation_to_strip)] if w.strip(punctuation_to_strip) in futures and futures[w.strip(punctuation_to_strip)] is not None else w
                    for w in text.split()
                ])
                self.values[k]=text
        print(f"\tafter values {self.values}")

    def extractValues(self,pattern:str,input:str):        
        regex_pattern = re.sub(r'\{(\w+)\}', r'(?P<\1>.+)', pattern)
        placeholders = re.findall(r'\{(\w+)\}', pattern)
        # Match the input string against the regex pattern
        match = re.match(regex_pattern, input)
        if match:
            # Populate self.values with placeholder keys and corresponding matched values
            self.values = {f'{{{name}}}': value for name, value in zip(placeholders, match.groups())}
            
            self.match = True
        else:
            # Clear values and set match to False if there's no match
            self.values = {}
            self.match = False

    @abstractmethod
    def handle(self,beliefSystem:HRIBeliefSystem) -> HRIResponse:
        pass


    def setAck(self,ack):        
        self.ack=ack

    def setOnFailure(self,onf):
        self.onf=onf

    def setOnSuccess(self,ons):
        self.ons=ons

    def setSocialPlanner(self,socialPlanner):
        self.socialPlanner=socialPlanner

    def setPerson(self, person):
        print(f"Setting person: {person}")  # Debug print
        self.person = person  # Fix the typo from self.perosn to self.person

    def setFutures(self, f:dict):
        self.futures=f


def sayAction(text,emotion="natural")->HRIAction:
    action = HRIAction(0,text,"say",emotion,{})
    #action.params.append(text.replace("_"," ")) 
    return action

def sayResponse(text,emotion="natural")->HRIResponse:
    actions=[sayAction(text,emotion)]    
    reason=""
    success=True
    missing_info=[]
    response=HRIResponse(actions,emotion,reason,success,missing_info)
    return response




class LLMLoader:
    _instances = {}  # Dictionary to store loaded LLM instances

    @staticmethod
    def load(key: str)->LLM:
        """
        Loads and returns an LLM instance based on the key.
        If the instance is already loaded, returns the cached instance.
        """
        if key in LLMLoader._instances:
            return LLMLoader._instances[key]
        
        # Get the configuration file path
        package_share_dir = get_package_share_directory('hri_framework')
        llms_config_path = os.path.join(
            package_share_dir, 'config', 'layers_config', 'llms_config.json'
        )
        
        # Load the JSON configuration
        with open(llms_config_path, 'r') as f:
            llms_config = json.load(f)
        
        # Get the module path from the config
        llm_module_path = llms_config.get(key)
        if not llm_module_path:
            return None  # Return None if the key is not found
        
        try:
            module_name, class_name = llm_module_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            LLMClass = getattr(module, class_name)
            instance = LLMClass()
            
            # Cache the instance
            LLMLoader._instances[key] = instance
            return instance
        except (ImportError, AttributeError) as e:
            print(f"Error loading LLM class for key '{key}': {e}")
            return None
