from abc import ABC, abstractmethod
from app.database import get_db_connection

class BaseModel(ABC):
    __tabela = None
    def __init__(self):
        self._id = None  # Será definido pelo banco
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @classmethod
    def buscar_por_id(cls, objeto_id, tabela):
        """Busca um objeto pelo ID e retorna um dicionário com os dados"""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {tabela} WHERE id = %s;", [objeto_id])
        dados = cur.fetchone()

        if dados:
            colunas = [desc[0] for desc in cur.description]  # Pegamos os nomes das colunas
            resultado = dict(zip(colunas, dados))  # Criamos um dicionário com {coluna: valor}
            cur.close()
            conn.close()
            return resultado
        
        cur.close()
        conn.close()
        return None

    @abstractmethod
    def salvar_no_banco(self):
        raise NotImplementedError("Cada subclasse precisa implementar salvar_no_banco()")

    def atualizar_dados(self,tabela,  **dados):
        if not self.id:
            raise ValueError("Objeto precisa ter um ID definido para atualizar.")
        
        conn = get_db_connection()
        cur = conn.cursor()

        campos = ', '.join(f"{campo} = %s" for campo in dados)
        valores = list(dados.values()) + [self.id]

        query = (f"UPDATE {tabela} SET {campos} WHERE id = %s")
        cur.execute(query, valores)

        conn.commit()
        cur.close()
        conn.close()

    def deletar_do_banco(self, tabela):
        if not self.id:
            raise ValueError("O objeto precisa ter um ID definido para ser deletado.")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"DELETE FROM {tabela} WHERE id = %s", (self.id,))
        conn.commit()

        cur.close()
        conn.close()

    @abstractmethod
    def exibir_info(self):
        raise NotImplementedError("Cada subclasse precisa implementar exibir_info()")
