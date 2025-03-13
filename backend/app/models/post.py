from app.models.basemodel import BaseModel
from app.database import get_db_connection

class Post(BaseModel):
    __tabela = "posts"

    def __init__(self, user_id, titulo, descricao, midia=None, id=None):
        super().__init__()
        self._id = id
        self.__user_id = user_id
        self.__titulo = titulo
        self.__descricao = descricao
        self.__midia = midia

    @property
    def user_id(self):
        return self.__user_id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def descricao(self):
        return self.__descricao

    @property
    def midia(self):
        return self.__midia

    def salvar_no_banco(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO posts (user_id, titulo, descricao, midia)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (self.user_id, self.titulo, self.descricao, self.midia))

        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def buscar_por_usuario(user_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, titulo, descricao, midia FROM posts WHERE user_id = %s;
        """, [user_id])

        posts = cur.fetchall()
        cur.close()
        conn.close()

        return [{"id": p[0], "titulo": p[1], "descricao": p[2], "midia": p[3]} for p in posts]

    @staticmethod
    def deletar_post(post_id):
        """
        Deleta o post com o ID informado utilizando o método deletar_do_banco do BaseModel.
        Retorna um dicionário com uma mensagem de sucesso ou um erro.
        """
        try:
            # Busca os dados do post pelo ID usando o método herdado de BaseModel
            post_data = Post.buscar_por_id(post_id, "posts")
            if not post_data:
                return {"erro": "Post não encontrado"}
            # Cria uma instância do post com os dados recuperados
            instance = Post(
                post_data['user_id'],
                post_data['titulo'],
                post_data['descricao'],
                post_data.get('midia'),
                id=post_data['id']
            )
            # Chama o método de deleção da classe BaseModel
            instance.deletar_do_banco(tabela="posts")
            return {"mensagem": "Post deletado com sucesso"}
        except Exception as e:
            return {"erro": f"Erro ao deletar post: {str(e)}"}
    
    def exibir_info(self):
        """Retorna as informações do post."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "midia": self.midia
        }
