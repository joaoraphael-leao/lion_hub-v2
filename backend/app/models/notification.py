from app.models.basemodel import BaseModel
from app.database import get_db_connection

class Notification(BaseModel):
    __tabela = "notifications"

    def __init__(self, usuario_id, tipo, objeto_id, lida=False, id=None):
        super().__init__()
        self._id = id
        self.__usuario_id = usuario_id
        self.__tipo = tipo  # Exemplo: "like", "comment", "follow"
        self.__objeto_id = objeto_id  # O ID do post/comentário/evento relacionado
        self.__lida = lida  # True ou False

    @staticmethod
    def get_tabela():
        return Notification.__tabela

    def salvar_no_banco(self):
        """Salva uma nova notificação no banco de dados"""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"""
            INSERT INTO {self.__tabela} (usuario_id, tipo, objeto_id, lida) 
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, [self.__usuario_id, self.__tipo, self.__objeto_id, self.__lida])

        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    def marcar_como_lida(self):
        """Marca a notificação como lida"""
        if not self.id:
            raise ValueError("A notificação precisa ter um ID para ser atualizada.")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"""
            UPDATE {self.__tabela} 
            SET lida = TRUE 
            WHERE id = %s;
        """, [self.id])

        conn.commit()
        cur.close()
        conn.close()

    def deletar_do_banco(self):
        """Remove a notificação do banco de dados"""
        if not self.id:
            raise ValueError("A notificação precisa ter um ID para ser deletada.")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"""
            DELETE FROM {self.__tabela} WHERE id = %s;
        """, [self.id])

        conn.commit()
        cur.close()
        conn.close()

    def exibir_info(self):
        """Exibe as informações da notificação"""
        return {
            "id": self.id,
            "usuario_id": self.__usuario_id,
            "tipo": self.__tipo,
            "objeto_id": self.__objeto_id,
            "lida": self.__lida
        }