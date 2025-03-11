from abc import ABC, abstractmethod


class HRIVerbalRequest:
    """
    This class contains the information relevant to a verbal request the interacting person has made
    given a person's verbal request in natural form, the HRI Toolkit will produce the relevant HRIVerbalRequest object
    associated to one of the patterns defined in the hri_config.json file.

    Attributes:
    rawText (str): the person's raw text e.g., "bring the bottle to bob"
    pattern (str): the pattern string, e.g., "bring the {object} to {who}"
    values (dict): the extracted values for the parameters in the pattern e.g., {"{object}":"bottle", "{who}":"bob"}
    emotion (str): the associated emotion (if) detected by the HRI toolkit    
    """
    def __init__(self,rawText:str, pattern:str,values:dict,emotion:str) -> None:
        self.rawText=rawText
        self.pattern=pattern
        self.values=values
        self.emotion=emotion
    
    def __repr__(self) -> str:
        return f"\n\traw text: {self.rawText}\n\tpattern: {self.pattern}\n\tvalues: {self.values}\n\temotion: {self.emotion}"

class HRIVisualRequest:
    """
    This class contains the information relevant to a visual request the interacting person has made
    given a person's visual request (gesture) in natural form, the HRI Toolkit will produce the relevant HRIVisualRequest object
    The HRI toolkit detects gestures either with its default gesture detection or user defined one.

    Attributes:
    gestureName (str): the name of the labeled gesture e.g., "pointing"
    poseDict (dict): a dictionary of [str,pose] that associates relevant ROS2 Pose objects, e.g., "left hand" with the vector it points to
    otherParams (dict): a dictionary of other parameters the gesture detector may provide     
    """
    def __init__(self,gestureName:str, poseDict:dict,otherParams:dict) -> None:
        self.gestureName=gestureName
        self.poseDict=poseDict
        self.otherParams=otherParams

    def __repr__(self) -> str:
        return f"\n\tgesture: {self.gestureName}\n\tposdict: {self.poseDict}\n\tother params: {self.otherParams}"

class HRIRequest:
    """
    HRI requests can be instructions, facts, queries or what ever a person has initiate.
    the HRI requests are constructed in the "Human Context" layer of the HRI toolkit, 
    and are later handled with assigned HRI Request Handlers - configured in the hri_config.json file
    given a person's request in natural form, the HRI Toolkit will produce the relevant HRIRequest object
    and activate its handler.
    
    Attributes:
    person (dict): the dictionary containing the interaction person information e.g., id, name, etc.
    verbalReq (HRIVerbalRequest): an object containing the verbal request attributes
    visualReq (HRIVisualRequest): an object containing the visual request attributes
    priority (int): lower is prioritized
    reactive (boolean): defines whether or not the request will also be handled by the Social Planning mechanism. reactive requests bypass this mechanism
    """
    def __init__(self,person:dict, verbalReq:HRIVerbalRequest, visualReq:HRIVisualRequest,priority:int) -> None:
        self.person=person
        self.verbalReq=verbalReq
        self.visualReq=visualReq
        self.priority=priority


class HRIBeliefSystem(ABC):
    """
    With HRI toolkit's implementation of this interface you can store and retrieve meaningful facts 
    about the robot, it's environment, people, objects and overall social context

    detected people and objects are automatically stored in the robot's belief system.
    you can retrieve data objects by their ids or associated attributes.
    
    for example, assume the following user instruction "bring the beautiful red bottle to bob".
    the HRI belief system can be asked to retrieve the information of "beautiful red bottle", and 
    a list of all bottles that are associated with these properties is returned. 

    an internal dedicated LLM is used for reasoning. for instance it can handel requests such as
    "bring the bottle with my favorite color to bob". 
    you can define the implementation of this llm in the llms.py file
    
    Methods:
    --------
    - updateRobotInfo(robot: dict):
        Update the belief system with new information about the robot.

    - updatePersonInfo(person: dict):
        Update the belief system with information about a person detected by the robot.

    - updateObjectInfo(object: dict):
        Update the belief system with details about an object detected by the robot.

    - get(type: str, description: str) -> list:
        Retrieve data objects from the belief system based on the provided type and description.
        the type can be person, robot or object

    """

    @abstractmethod
    def updateRobotInfo(self, robot: dict):
        """
        Update the belief system with new information about the robot.

        Parameters:
        -----------
        robot : dict
            A dictionary containing details about the robot's current status, such as its location, 
            capabilities, or internal states (e.g., battery level, hardware status).
        
        Example:
        --------
        robot_info = {
            "id": 1,
            "location": "kitchen",
            "battery": 85
        }
        belief_system.updateRobotInfo(robot_info)
        """
        pass

    @abstractmethod
    def updatePersonInfo(self, person: dict):
        """
        Update the belief system with information about a person detected by the robot.

        Parameters:
        -----------
        person : dict
            A dictionary containing details about the detected person, including their name, location, 
            or any distinguishing features (e.g., clothing, hair color, facial recognition data).

        Example:
        --------
        person_info = {
            "id": 353,
            "name": "Bob",
            "location": "living room",
            "attributes": ["male", "wearing glasses"]
        }
        belief_system.updatePersonInfo(person_info)
        """
        pass

    @abstractmethod
    def updateObjectInfo(self, object: dict):
        """
        Update the belief system with details about an object detected by the robot.

        Parameters:
        -----------
        object : dict
            A dictionary containing information about the detected object, such as its type, color, 
            location, or other relevant attributes.

        Example:
        --------
        object_info = {
            "id": 3,
            "label": "bottle",
            "color": "red",
            "attributes": ["beautiful", "fragile"]
        }
        belief_system.updateObjectInfo(object_info)
        """
        pass

    @abstractmethod
    def get(self, type: str, description: str) -> list:
        """
        Retrieve objects from the belief system based on their type and description.

        This method queries the belief system and returns a list of objects that match the given 
        type and description. For example, asking for "bottle" with the description "beautiful red" 
        might return all objects of type "bottle" that have been identified as both beautiful and red.

        Parameters:
        -----------
        type : str
            The type of object to search for (e.g., "person", "robot", "object").
        description : str
            A description of the object to be retrieved (e.g., attributes like "red", "beautiful", 
            "fragile").

        Returns:
        --------
        list:
            A list of objects matching the given type and description. Each object in the list is 
            represented as a dictionary containing its attributes (e.g., id, location, type).

        Example:
        --------
        objects = belief_system.get("bottle", "beautiful red")
        print(objects)
        # Output: [{"id": "object1", "type": "bottle", "color": "red", "location": "table", "attributes": ["beautiful", "fragile"]}]
        """
        pass

    @abstractmethod
    def getRobot(self)->dict:
        pass


class HRIResponse:
    """
    This class represents the response generated after processing an HRIRequest.

    The response includes information on actions or utterances the robot should perform, 
    the emotional tone to adopt, reasoning behind the response, and whether the request 
    was successfully interpreted. Additionally, it lists any missing information required 
    to fully handle the request.

    Attributes:
    -----------
    actions : list of str
        A sequence of textual descriptions representing actions or speech the robot should execute. 
        For example, ["go to location (x,y,z)", "say 'Here is the bottle'"].
    
    emotion : str
        The emotion associated with the response. This could influence how the robot speaks or moves 
        while performing actions (e.g., "happy", "neutral", "frustrated").

    reason : str
        The reasoning or justification behind the response. It explains why the robot has decided on 
        the given actions or behavior. For example, "Object not found in the environment."

    success : bool
        Indicates whether the request was successfully interpreted and handled. If False, 
        the response might contain further clarification requests or suggestions.

    missing_info : list of str
        A list of information or attributes that were required but missing in order to fully process 
        the request. For example, ["object color", "destination location"].

    Methods:
    --------
    __init__(self, actions: list, emotion: str, reason: str, success: bool, missing_info: list) -> None:
        Initializes the HRIResponse object with the provided attributes.
    """

    def __init__(self, actions: list, emotion: str, reason: str, success: bool, missing_info: list) -> None:
        """
        Initializes the HRIResponse object.

        Parameters:
        -----------
        actions : list of str
            A sequence of textual descriptions representing actions or speech the robot should execute.

        emotion : str
            The emotion associated with the response, such as "happy", "neutral", "frustrated", etc.

        reason : str
            The reasoning or justification behind the response.

        success : bool
            A boolean indicating whether the request was successfully interpreted.

        missing_info : list of str
            A list of missing attributes or details required to fully process the request.
        """
        self.actions = actions
        self.emotion = emotion
        self.reason = reason
        self.success = success
        self.missing_info = missing_info


class HRIRequestHandler(ABC):
    """
    Interface for handling HRIRequests.

    The request handler processes an HRIRequest, which may include both verbal and visual components, 
    and generates an appropriate HRIResponse. The response provides the necessary actions the robot should take, 
    the emotional tone, reasoning, and any missing information required to fulfill the request.

    Methods:
    --------
    handle_request(self, request: HRIRequest, , beliefSystem:HRIBeliefSystem) -> HRIResponse:
        Processes the given HRIRequest w.r.t hri belief system and returns an HRIResponse.
    """

    @abstractmethod
    def handle_request(self, request: HRIRequest, beliefSystem:HRIBeliefSystem) -> HRIResponse:
        """
        Processes the given HRIRequest and returns an HRIResponse.

        Parameters:
        -----------
        request : HRIRequest
            The HRIRequest object containing the person's verbal and visual requests, as well as 
            information about the person making the request.
        
        beliefSystem: HRIBeliefSystem
            a reference to the belief system of the robot to store or retrieve relevant information

        Returns:
        --------
        HRIResponse:
            A response object containing a sequence of actions, associated emotion, reasoning, success status, 
            and a list of any missing information required to handle the request.

        Example:
        --------
        request = HRIRequest(person=person_data, verbalReq=verbal_request, visualReq=visual_request)
        response = handler.handle_request(request)
        print(response.actions)
        # Output: ["move to living room", "say 'I am bringing the bottle'"]
        """
        pass