from decision_helper import DecisionHelper
from hri_framework.Context_Management.decision_helpers_dir.decision_helper import Decision
from hri_framework.Context_Management.managers.availability_manager import AvailabilityManager


##
# @brief This class is a decision helper that checks if a user is available
#
class UserAvailabilityDecisionHelper(DecisionHelper):


    def copy(self):
        pass


    def decide(self, req: HRIRequest) -> Decision:

        # TODO: need to extract the person for which availability check is needed
        person = req.person

        if person is None:
            return Decision(False, 0, "neutral", "You did not specify a person")

        if AvailabilityManager().is_available(person):
            return Decision(True, 0, "neutral", f"{person} is available")

        return Decision(False, 0, "neutral", f"{person} is not available")
