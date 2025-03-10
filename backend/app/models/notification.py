from app.models.basemodel import BaseModel
from app.database import get_db_connection

class Notification(BaseModel):
    __tabela = "notifications"  # Define a tabela correspondente no banco

    def __init__(self, usuario_id, tipo, objeto_id, lida=False):
        super().__init__()
        self.usuario_id = usuario_id  # Quem recebe a notificação
        self.tipo = tipo  # Exemplo: 'like', 'comment', 'follow', 'message'
        self.objeto_id = objeto_id  # ID do post, comentário ou seguidor relacionado
        self.lida = lida  # Estado da notificação (True/False)

    def salvar_no_banco(self):
        """Salva a notificação no banco de dados"""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO notifications (usuario_id, tipo, objeto_id, lida) VALUES (%s, %s, %s, %s) RETURNING id",
            (self.usuario_id, self.tipo, self.objeto_id, self.lida),
        )
        self.id = cur.fetchone()[0]  # Obtém o ID gerado pelo banco
        conn.commit()
        cur.close()
        conn.close()

    def marcar_como_lida(self):
        """Marca a notificação como lida"""
        self.atualizar_dados(lida=True)

    def exibir_info(self):
        """Retorna um dicionário com os detalhes da notificação"""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo,
            "objeto_id": self.objeto_id,
            "lida": self.lida,
        }
