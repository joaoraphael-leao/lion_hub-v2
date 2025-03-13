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

    @staticmethod
    def buscar_por_post(post_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT comments.id, comments.autor_id, users.nome, comments.conteudo, comments.data_criacao 
            FROM comments
            JOIN users ON comments.autor_id = users.id
            WHERE comments.post_id = %s ORDER BY comments.data_criacao ASC;
        """, [post_id])

        comentarios = cur.fetchall()
        cur.close()
        conn.close()

        return [{"id": c[0], "autor_id": c[1], "autor_nome": c[2], "conteudo": c[3], "data": c[4]} for c in comentarios]

    @staticmethod
    def deletar_comentario(comentario_id, autor_id):
        """
        Deleta o comentário com o ID informado, verificando se o autor
        do comentário é o mesmo que está solicitando a deleção.
        Retorna um dicionário com uma mensagem de sucesso ou com um erro.
        """
        try:
            # Busca os dados do comentário (usando o método herdado da BaseModel)
            comment_data = Comment.buscar_por_id(comentario_id)
            if not comment_data:
                return {"erro": "Comentário não encontrado"}
            # Verifica se o autor do comentário é o mesmo que solicitou a deleção
            if comment_data["autor_id"] != autor_id:
                return {"erro": "Você não tem permissão para deletar este comentário."}
            # Cria uma instância do comentário para chamar o método de deleção
            instance = Comment(
                comment_data["post_id"],
                comment_data["autor_id"],
                comment_data["conteudo"],
                id=comment_data["id"]
            )
            instance.deletar_do_banco(tabela="comments")
            return {"mensagem": "Comentário deletado com sucesso"}
        except Exception as e:
            return {"erro": f"Erro ao deletar comentário: {str(e)}"}

    def salvar_no_banco(self):
        """
        Salva o comentário no banco de dados.
        Insere os valores de post_id, autor_id e conteudo na tabela e atualiza o atributo id com o valor gerado.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        # Insere o comentário e retorna o id gerado
        cur.execute(
            f"INSERT INTO {Comment.__tabela} (post_id, autor_id, conteudo) VALUES (%s, %s, %s) RETURNING id;",
            (self.__post_id, self.__autor_id, self.__conteudo)
        )
        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    def exibir_info(self):
        """
        Retorna um dicionário com as informações do comentário.
        """
        return {
            "id": self.id,
            "post_id": self.__post_id,
            "autor_id": self.__autor_id,
            "conteudo": self.__conteudo
        }