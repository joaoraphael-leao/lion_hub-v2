from abc import ABC, abstractmethod
import Terminal.storage as storage

# Classe abstrata mãe de Group e Event.
class Community(ABC):
    def __init__(self, name, description, owner):
        self.__name = name
        self.__description = description
        self.__owner = owner
        self.__members = [owner]

    def see_members(self):
        for member in self.__members:
            print(member)

    @property
    def members(self):
        return self.__members
    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description
    @property
    def owner(self):
        return self.__owner

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()

    @abstractmethod
    def manage_community(self):
        raise NotImplementedError()

    def add_member(self, member):
        if member not in self.__members:
            self.__members.append(member)
            print("Usuário adicionado com sucesso.")
            return
        print("Usuário já é membro da comunidade.")

    def remove_member(self, remover_member, removed_member):
        if removed_member == self.__owner:
            print("O dono da comunidade não pode ser removido.")
        if remover_member == self.__owner:
            try:
                self.__members.remove(remover_member)
                print("Usuário removido com sucesso.")
            except ValueError:
                print("Usuário não encontrado.")

class Event(Community):
    def __init__(self, name, description, owner, event_date, event_location):
        super().__init__(name, description, owner)
        self.__event_date = event_date
        self.__event_location = event_location
        # Usa o contador global de IDs para eventos
        self.__id = storage.event_id_counter
        storage.event_id_counter += 1
    def __str__(self):
        print(f"Evento {self.__id}: {self.__name}\n"
              f"    Data: {self.__event_date}\n"
              f"    Local: {self.__event_location}\n"
              f"    Descrição: {self.__description}\n"
              f"    Owner: {self.__owner}")

    @property
    def event_date(self):
        return self.__event_date
    @property
    def event_location(self):
        return self.__event_location
    @property
    def id(self):
        return self.__id

class Group(Community):
    def __init__(self, name, description, owner):
        super().__init__(name, description, owner)
        self.__posts = []
        self.__messages = []
        # Usa o contador global de IDs para grupos
        self.__id = storage.group_id_counter
        storage.group_id_counter += 1

    def
