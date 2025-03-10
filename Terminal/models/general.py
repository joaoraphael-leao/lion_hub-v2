from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self):
        self.model = None

    @abstractmethod
    def create(self):
        raise NotImplementedError()

    @abstractmethod
    def see_info(self):
        raise NotImplementedError()

    @abstractmethod
    def manage(self):
        raise NotImplementedError()

    @abstractmethod
    def delete(self):
        raise NotImplementedError()




