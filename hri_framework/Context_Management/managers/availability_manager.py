
class AvailabilityManager:

    availability_state = dict()


    def _on_new_person_appeared(self, hri_id:str):
        self.availability_state[hri_id] = {"present": True, "availability_score": 0.5}


    def _on_person_disappeared(self, hri_id:str):
        self.availability_state[hri_id]["present"] = False
        self.availability_state[hri_id]["availability_score"] = max(self.availability_state[hri_id]["availability_score"] - 0.1, 0.0)


    def _on_person_present(self, hri_id:str):
        self.availability_state[hri_id]["present"] = True
        self.availability_state[hri_id]["availability_score"] = min(self.availability_state[hri_id]["availability_score"] + 0.1, 1.0)


    def _update_present_person_availability(self, hri_id:str):
        if hri_id not in self.availability_state:
            self._on_new_person_appeared(hri_id)
        else:
            self._on_person_present(hri_id)


    def handle_persons(self, persons:dict) -> dict:
        for person in persons:
            self._update_present_person_availability(person["hri_id"])

        for hri_id in self.availability_state:
            if hri_id not in persons:
                self._on_person_disappeared(hri_id)

        return self.availability_state
