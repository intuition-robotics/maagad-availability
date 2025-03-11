from event_handlers import EventHandler
from hri_framework.Context_Management.managers.availability_manager import AvailabilityManager


##
# @brief This class is an event handler that handles user presence events
# and updates the availability of the user in the AvailabilityManager
#
class UserPresenceEventHandler(EventHandler):

    def handle(self, beliefSystem: HRIBeliefSystem) -> HRIResponse:

        # TODO: need to understand how to extract the computer vision data from the belief system
        for person in beliefSystem.get_data("computer_vision_data"):
            AvailabilityManager().set_availability(person.name, person.is_seen)

        # TODO: need to understand what is the HRIResponse and what needs to be returned from here
        return HRIResponse()
