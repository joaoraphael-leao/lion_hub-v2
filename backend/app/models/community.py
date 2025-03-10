from app.models.basemodel import BaseModel
from abc import ABC, abstractmethod

class CommunityEntity(BaseModel, ABC):
    """Classe base para Group e Event."""
    __tabela = None  # Definido nas subclasses

    def __init__(self, owner_id, nome, descricao, privacidade=True, id=None):
        super().__init__()
        self._id = id
        self.__owner_id = owner_id
        self.__nome = nome
        self.__descricao = descricao
        self.__privacidade = privacidade  # True = Público, False = Privado

    @property
    def owner_id(self):
        return self.__owner_id

    @property
    def nome(self):
        return self.__nome

    @property
    def descricao(self):
        return self.__descricao

    @property
    def privacidade(self):
        return self.__privacidade

    def tornar_privado(self):
        """Define o grupo/evento como privado."""
        self.__privacidade = False
        self.atualizar_dados(privacidade=False)

    def tornar_publico(self):
        """Define o grupo/evento como público."""
        self.__privacidade = True
        self.atualizar_dados(privacidade=True)

    @abstractmethod
    def exibir_info(self):
        """Cada subclasse implementa seu próprio exibir_info()."""
        pass


class Group(CommunityEntity):
    """Representa um grupo na rede social."""
    __tabela = "groups"

    def __init__(self, owner_id, nome, descricao, privacidade=True, id=None):
        super().__init__(owner_id, nome, descricao, privacidade, id)

    def exibir_info(self):
        """Retorna informações do grupo"""
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "nome": self.nome,
            "descricao": self.descricao,
            "privacidade": self.privacidade
        }


class Event(CommunityEntity):
    """Representa um evento na rede social."""
    __tabela = "events"

    def __init__(self, owner_id, nome, descricao, data, localizacao, privacidade=True, id=None):
        super().__init__(owner_id, nome, descricao, privacidade, id)
        self.__data = data
        self.__localizacao = localizacao

    @property
    def data(self):
        return self.__data

    @property
    def localizacao(self):
        return self.__localizacao

    def exibir_info(self):
        """Retorna informações do evento"""
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "nome": self.nome,
            "descricao": self.descricao,
            "data": self.data,
            "localizacao": self.localizacao,
            "privacidade": self.privacidade
        }