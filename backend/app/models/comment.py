from app.models.basemodel import BaseModel
from app.database import get_db_connection

class Comment(BaseModel):
    __tabela = "comments"

    def __init__(self, post_id, autor_id, conteudo, id=None):
        super().__init__()
        self._id = id
        self.__post_id = post_id
        self.__autor_id = autor_id
        self.__conteudo = conteudo

    @property
    def post_id(self):
        return self.__post_id

    @property
    def autor_id(self):
        return self.__autor_id

    @property
    def conteudo(self):
        return self.__conteudo

    def salvar_no_banco(self):
        """Salva um novo comentário no banco de dados."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO comments (post_id, autor_id, conteudo)
            VALUES (%s, %s, %s) RETURNING id;
        """, [self.post_id, self.autor_id, self.conteudo])

        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    def atualizar_comentario(self, novo_conteudo):
        """Edita um comentário, garantindo que apenas o autor possa alterá-lo."""
        self.__conteudo = novo_conteudo
        self.atualizar_dados(conteudo=novo_conteudo)

    @staticmethod
    def deletar_comentario(comment_id, autor_id):
        """Permite que apenas o autor do comentário o exclua."""
        conn = get_db_connection()
        cur = conn.cursor()

        # Verifica se o usuário é o autor do comentário
        cur.execute("""
            SELECT autor_id FROM comments WHERE id = %s;
        """, [comment_id])
        resultado = cur.fetchone()

        if not resultado:
            return {"erro": "Comentário não encontrado."}
        if resultado[0] != autor_id:
            return {"erro": "Você não tem permissão para excluir este comentário."}

        cur.execute("""
            DELETE FROM comments WHERE id = %s;
        """, [comment_id])
        conn.commit()

        cur.close()
        conn.close()
        return {"mensagem": "Comentário excluído com sucesso."}

    @staticmethod
    def buscar_por_post(post_id):
        """Busca todos os comentários de um post específico."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, autor_id, conteudo, data_criacao FROM comments
            WHERE post_id = %s ORDER BY data_criacao ASC;
        """, [post_id])

        comentarios = cur.fetchall()
        cur.close()
        conn.close()

        return [{"id": c[0], "autor_id": c[1], "conteudo": c[2], "data": c[3]} for c in comentarios]

    def exibir_info(self):
        """Exibe detalhes do comentário."""
        return {
            "id": self.id,
            "post_id": self.post_id,
            "autor_id": self.autor_id,
            "conteudo": self.conteudo
        }