from app.models.basemodel import BaseModel
from app.database import get_db_connection

class Like(BaseModel):
    __tabela = "likes"

    def __init__(self, usuario_id, post_id, id=None):
        """
        Representa uma curtida em um post.
        :param usuario_id: ID do usuário que curtiu
        :param post_id: ID do post curtido
        """
        super().__init__()
        self._id = id
        self.__usuario_id = usuario_id
        self.__post_id = post_id

    @property
    def usuario_id(self):
        return self.__usuario_id

    @property
    def post_id(self):
        return self.__post_id

    def salvar_no_banco(self):
        """Salva a curtida no banco de dados."""
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO likes (usuario_id, post_id)
                VALUES (%s, %s) ON CONFLICT DO NOTHING RETURNING id;
            """, [self.usuario_id, self.post_id])

            resultado = cur.fetchone()
            if resultado:
                self.id = resultado[0]
                conn.commit()
                return {"mensagem": "Curtida registrada com sucesso."}
            else:
                return {"erro": "Você já curtiu este post."}
        except Exception as e:
            return {"erro": str(e)}
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def descurtir(usuario_id, post_id):
        """Remove a curtida do usuário em um post."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM likes WHERE usuario_id = %s AND post_id = %s;
        """, [usuario_id, post_id])
        conn.commit()

        cur.close()
        conn.close()
        return {"mensagem": "Curtida removida com sucesso."}

    @staticmethod
    def verificar_curtida(usuario_id, post_id):
        """Verifica se um usuário já curtiu um post."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 1 FROM likes WHERE usuario_id = %s AND post_id = %s;
        """, [usuario_id, post_id])
        resultado = cur.fetchone()

        cur.close()
        conn.close()
        return resultado is not None  # Retorna True se já curtiu, False caso contrário

    @staticmethod
    def contar_curtidas(post_id):
        """Conta quantas curtidas um post tem."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) FROM likes WHERE post_id = %s;
        """, [post_id])
        total = cur.fetchone()[0]

        cur.close()
        conn.close()
        return total

    def exibir_info(self):
        """Retorna informações sobre a curtida."""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "post_id": self.post_id
        }