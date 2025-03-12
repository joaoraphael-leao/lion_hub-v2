from abc import ABC, abstractmethod
from app.database import get_db_connection

class BaseModel(ABC):
    def __init__(self):
        self._id = None  # Será definido pelo banco
        
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @classmethod
    def buscar_por_id(cls, objeto_id, tabela):
        """Busca um objeto pelo ID e retorna um dicionário com os dados"""
        if not tabela:
            raise ValueError(f"Tabela {tabela} não definida")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {tabela} WHERE id = %s;", [objeto_id])
        dados = cur.fetchone()

        cur.close()
        conn.close()

        if dados:
            colunas = [desc[0] for desc in cur.description]  # Pegamos os nomes das colunas
            return dict(zip(colunas, dados))  # Criamos um dicionário com {coluna: valor}
        
        return None

    @abstractmethod
    def salvar_no_banco(self):
        raise NotImplementedError("Cada subclasse precisa implementar salvar_no_banco()")

    def atualizar_dados(classe, **dados):
        if not classe.id:
            raise ValueError("Objeto precisa ter um ID definido para atualizar.")
        if not classe.get_tabela:
            raise ValueError("Classe filha precisa definir o nome da tabela.")

        conn = get_db_connection()
        cur = conn.cursor()

        campos = ', '.join(f"{campo} = %s" for campo in dados)
        valores = list(dados.values()) + [classe._id]

        query = f"UPDATE {classe.get_tabela()} SET {campos} WHERE id = %s"
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