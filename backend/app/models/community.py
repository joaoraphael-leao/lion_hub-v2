from app.models.basemodel import BaseModel
from abc import ABC, abstractmethod

class CommunityEntity(BaseModel, ABC):
    """Classe base para Group e Event."""
    def __init__(self, user_id, nome, descricao, privacidade=True, id=None):
        super().__init__()
        self._id = id
        self.__user_id = user_id
        self.__nome = nome
        self.__descricao = descricao
        self.__privacidade = privacidade  # True = Público, False = Privado

    @property
    def user_id(self):
        return self.__user_id

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
    def __init__(self, user_id, nome, descricao, privacidade=True, id=None):
        super().__init__(user_id, nome, descricao, privacidade, id)

   

    def exibir_info(self):
        """Retorna informações do grupo."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "nome": self.nome,
            "descricao": self.descricao,
            "privacidade": self.privacidade
        }

    @staticmethod
    def buscar_por_usuario(user_id):
        """
        Busca todos os grupos cujo owner_id seja o usuário informado.
        Retorna uma lista de dicionários com os dados dos grupos.
        """
        tabela = Group.get_tabela()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"SELECT id, user_id, nome, descricao, privacidade FROM {tabela} WHERE user_id = %s;",
            [user_id]
        )
        grupos = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {"id": g[0], "user_id": g[1], "nome": g[2], "descricao": g[3], "privacidade": g[4]}
            for g in grupos
        ]
    
    def salvar_no_banco(self):
        """Salva o grupo no banco de dados e atualiza o atributo id."""
        conn = get_db_connection()
        cur = conn.cursor()
        tabela = self.get_tabela()
        cur.execute(
            f"INSERT INTO {tabela} (user_id, nome, descricao, privacidade) VALUES (%s, %s, %s, %s) RETURNING id;",
            (self.user_id, self.nome, self.descricao, self.privacidade)
        )
        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

class Event(CommunityEntity):
    """Representa um evento na rede social."""
    def __init__(self, user_id, nome, descricao, data, localizacao, privacidade=True, id=None):
        super().__init__(user_id, nome, descricao, privacidade, id)
        self.__data = data
        self.__localizacao = localizacao

    @property
    def data(self):
        return self.__data

    @property
    def localizacao(self):
        return self.__localizacao

    def exibir_info(self):
        """Retorna informações do evento."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "nome": self.nome,
            "descricao": self.descricao,
            "data": self.data,
            "localizacao": self.localizacao,
            "privacidade": self.privacidade
        }
    def salvar_no_banco(self):
        """Salva o evento no banco de dados e atualiza o atributo id."""
        conn = get_db_connection()
        cur = conn.cursor()
        # Neste exemplo, a tabela é definida como 'events'
        tabela = "events"
        cur.execute(
            f"INSERT INTO {tabela} (user_id, nome, descricao, data, localizacao, privacidade) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
            (self.user_id, self.nome, self.descricao, self.data, self.localizacao, self.privacidade)
        )
        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
    @staticmethod
    def buscar_por_usuario(user_id):
        """
        Busca todos os eventos cujo owner_id seja o usuário informado.
        Retorna uma lista de dicionários com os dados dos eventos.
        """
        tabela = "events"  # ou use um método similar a get_tabela() se preferir
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"SELECT id, user_id, nome, descricao, data, localizacao, privacidade FROM {tabela} WHERE user_id = %s;",
            [user_id]
        )
        eventos = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                "id": e[0],
                "user_id": e[1],
                "nome": e[2],
                "descricao": e[3],
                "data": e[4],
                "localizacao": e[5],
                "privacidade": e[6]
            }
            for e in eventos
        ]