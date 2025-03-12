from app.models.basemodel import BaseModel
from app.database import get_db_connection

class Message(BaseModel):
    __tabela = "messages"

    def __init__(self, remetente_id, destinatario_id, conteudo, id=None, lida=False):
        super().__init__()
        self._id = id
        self.__remetente_id = remetente_id
        self.__destinatario_id = destinatario_id
        self.__conteudo = conteudo
        self.__lida = lida

    @property
    def remetente_id(self):
        return self.__remetente_id
        
    @property
    def destinatario_id(self):
        return self.__destinatario_id

    @property
    def conteudo(self):
        return self.__conteudo

    @property
    def lida(self):
        return self.__lida

    def salvar_no_banco(self):
        """Salva a mensagem no banco de dados."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO messages (remetente_id, destinatario_id, conteudo, lida)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, [self.remetente_id, self.destinatario_id, self.conteudo, self.lida])

        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def buscar_historico(remetente_id, destinatario_id):
        """Retorna todas as mensagens trocadas entre dois usuários."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, remetente_id, destinatario_id, conteudo, lida, data_criacao
            FROM messages
            WHERE (remetente_id = %s AND destinatario_id = %s)
               OR (remetente_id = %s AND destinatario_id = %s)
            ORDER BY data_criacao ASC;
        """, [remetente_id, destinatario_id, destinatario_id, remetente_id])

        mensagens = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {
                "id": msg[0],
                "remetente_id": msg[1],
                "destinatario_id": msg[2],
                "conteudo": msg[3],
                "lida": msg[4],
                "data_criacao": msg[5]
            }
            for msg in mensagens
        ]

    @staticmethod
    def marcar_como_lida(mensagem_id):
        """Marca uma mensagem como lida."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE messages SET lida = TRUE WHERE id = %s;
        """, [mensagem_id])
        conn.commit()

        cur.close()
        conn.close()
        return {"mensagem": "Mensagem marcada como lida."}

    @staticmethod
    def deletar_mensagem(mensagem_id, usuario_id):
        """Deleta uma mensagem, garantindo que apenas o remetente ou destinatário possa excluir."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM messages WHERE id = %s AND (remetente_id = %s OR destinatario_id = %s);
        """, [mensagem_id, usuario_id, usuario_id])
        conn.commit()

        cur.close()
        conn.close()
        return {"mensagem": "Mensagem excluída com sucesso."}

    def exibir_info(self):
        """Retorna informações sobre a mensagem."""
        return {
            "id": self.id,
            "remetente_id": self.remetente_id,
            "destinatario_id": self.destinatario_id,
            "conteudo": self.conteudo,
            "lida": self.lida
        }