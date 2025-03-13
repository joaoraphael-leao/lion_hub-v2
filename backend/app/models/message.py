from app.models.basemodel import BaseModel
from app.database import get_db_connection

class Message(BaseModel):
    __tabela = "messages"

    def __init__(self, remetente_id, destinatario_id, conteudo, id=None):
        super().__init__()
        self._id = id
        self.__remetente_id = remetente_id
        self.__destinatario_id = destinatario_id
        self.__conteudo = conteudo


    @property
    def remetente_id(self):
        return self.__remetente_id
        
    @property
    def destinatario_id(self):
        return self.__destinatario_id

    @property
    def conteudo(self):
        return self.__conteudo

    def salvar_no_banco(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO messages (remetente_id, destinatario_id, conteudo)
            VALUES (%s, %s, %s) RETURNING id;
        """, [self.remetente_id, self.destinatario_id, self.conteudo])
        
        result = cur.fetchone()
        if result:
            self.id = result[0]
        else:
            raise Exception("Erro ao inserir mensagem no banco: nenhum ID retornado.")
        
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def buscar_historico(remetente_id, destinatario_id, usuario_id):
        """Retorna todas as mensagens entre dois usuários, validando permissões."""
        if usuario_id not in [remetente_id, destinatario_id]:
            return {"erro": "Você não tem permissão para ver essas mensagens."}

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, remetente_id, destinatario_id, conteudo, data_criacao
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
                "data_criacao": msg[4]
            }
            for msg in mensagens
        ]

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
        }