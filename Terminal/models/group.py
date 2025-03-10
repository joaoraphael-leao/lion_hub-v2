from Terminal.storage import groups, group_id_counter


class Group:
    def __init__(self, name, description, founder):
        self._name = name
        self._description = description
        self._posts = []
        self._messages = []
        # Usa o contador global de IDs para grupos
        self._id = group_id_counter
        group_id_counter += 1

    def __str__(self):
        return f"{self._name} - {len(self._members)} Participantes"

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getFounder(self):
        return self._founder

    def getMembers(self):
        return self._members

    def addMember(self, member):
        if member not in self._members:
            self._members.append(member)
            return True
        return False

    def removeMember(self, member):
        if member in self._members and member != self._founder:
            self._members.remove(member)
            return True
        return False