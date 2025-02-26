from storage import events
import storage

class Event:
    def __init__(self, event_name, event_date, event_location, event_description):
        self._event_name = event_name
        self._event_date = event_date
        self._event_location = event_location
        self._event_description = event_description
        self._participants = []
        # Usa o contador global de IDs para eventos
        self._id = storage.event_id_counter
        storage.event_id_counter += 1

    def __str__(self):
        return (f"Evento {self._id}: {self._event_name}\n"
                f"    Data: {self._event_date}\n"
                f"    Local: {self._event_location}\n"
                f"    Descrição: {self._event_description}")

    def getId(self):
        return self._id

    def getEventName(self):
        return self._event_name

    def getEventDate(self):
        return self._event_date

    def getParticipants(self):
        return self._participants

    def addParticipant(self, user):
        if user not in self._participants:
            self._participants.append(user)