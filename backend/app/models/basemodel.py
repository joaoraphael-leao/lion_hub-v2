from abc import ABC, abstractmethod
from database import get_db_connection

class BaseModel(ABC):
    __tabela = None  # Definido nas subclasses

    def __init__(self):
        self._id = None  # Será definido pelo banco
        
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @abstractmethod
    def salvar_no_banco(self):
        raise NotImplementedError("Cada subclasse precisa implementar salvar_no_banco()")

    def atualizar_dados(self, **dados):
        if not self.id:
            raise ValueError("Objeto precisa ter um ID definido para atualizar.")
        if not self.__tabela:
            raise ValueError("Classe filha precisa definir o nome da tabela.")

        conn = get_db_connection()
        cur = conn.cursor()

        campos = ', '.join(f"{campo} = %s" for campo in dados)
        valores = list(dados.values()) + [self._id]

        query = f"UPDATE {self.__tabela} SET {campos} WHERE id = %s"
        cur.execute(query, valores)

        conn.commit()
        cur.close()
        conn.close()

    def deletar_do_banco(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"DELETE FROM {self.__tabela} WHERE id = %s", (self._id,))
        conn.commit()

        cur.close()
        conn.close()
    
    @abstractmethod
    def exibir_info(self):
        raise NotImplementedError("Cada subclasse precisa implementar exibir_info()")