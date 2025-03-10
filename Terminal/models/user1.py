from Terminal.models.general import BaseModel
import Terminal.storage as storage

class User(BaseModel):
    def __init__(self, name, email, password):
        self.__name = name
        self.__email = email
        self.__password = password
        self.__id = storage.user_id_counter
        storage.user_id_counter += 1






class privateProfile:
    def __init__(self, name, email, password):
        self.__name = name
        self.__email = email
        self.__password = password
        self.__id = storage.user_id_counter
        storage.user_id_counter += 1

