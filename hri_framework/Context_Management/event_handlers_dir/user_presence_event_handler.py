from event_handlers import EventHandler
from hri_framework.Context_Management.managers.availability_manager import AvailabilityManager
from hri_framework.Context_Management.requests.hri_request_handlers import HRIBeliefSystem, HRIResponse

##
# @brief This class is an event handler that handles user presence events
# and updates the availability of the user in the AvailabilityManager
#
class UserPresenceEventHandler(EventHandler):

    def handle(self, belief_system: HRIBeliefSystem) -> HRIResponse | None:

        persons = belief_system.get("person", "presence")

        for person in persons:
            AvailabilityManager().set_availability(person["id"], person["presence"])

        return None
