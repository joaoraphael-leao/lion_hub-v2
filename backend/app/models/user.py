from app.models.basemodel import BaseModel
from app.database import get_db_connection

class User(BaseModel):

    def __init__(self, nome, email, senha, id=None):
        super().__init__()
        self._id = id
        self.__nome = nome
        self.__email = email
        self.__senha = senha  # Armazenando a senha em texto plano
        __tabela = "users"

    @property
    def nome(self):
        return self.__nome

    @property
    def email(self):
        return self.__email

    @property
    def senha(self):
        return self.__senha

    def tornar_privado(self):
        """Altera o perfil para privado e atualiza no banco de dados."""
        self.__privacidade = False
        self.atualizar_dados("users", privacidade=False)

    def tornar_publico(self):
        """Altera o perfil para público e atualiza no banco de dados."""
        self.__privacidade = True
        self.atualizar_dados("users", privacidade=True)
        c
    def verificar_senha(self, senha):
        # Comparação direta de senhas em texto plano
        return senha == self.__senha

    @classmethod
    def buscar_por_email(cls, email):
        """Busca um usuário pelo e-mail."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, nome, email, senha FROM users WHERE email = %s;", [email])
        dados = cur.fetchone()

        cur.close()
        conn.close()

        if dados:
            # Criando o objeto User com a senha em texto plano
            usuario = cls(dados[1], dados[2], dados[3], id=dados[0])
            return usuario
        return None

    def salvar_no_banco(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (nome, email, senha, privacidade) 
            VALUES (%s, %s, %s, True) RETURNING id;
        """, [self.nome, self.email, self.__senha])  # Salvando a senha em texto plano

        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    def atualizar_usuario(self, nome=None, senha=None):
        dados = {}
        if nome:
            dados["nome"] = nome
            self.__nome = nome
        if senha:
            dados["senha"] = senha  # Atualizando a senha em texto plano
            self.__senha = senha
        if dados:
            self.atualizar_dados("users", **dados)

    def exibir_info(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM followers WHERE seguido_id = %s;
        """, [self.id])
        seguidores = cur.fetchone()[0]
        cur.close()
        conn.close()

        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "seguidores": seguidores
        }

    def ver_seguidores(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT users.id, users.nome
            FROM followers
            JOIN users ON followers.seguidor_id = users.id
            WHERE followers.seguido_id = %s;
        """, [self.id])

        seguidores = cur.fetchall()
        cur.close()
        conn.close()

        return [{"id": row[0], "nome": row[1]} for row in seguidores]

    def ver_seguindo(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT users.id, users.nome
            FROM followers
            JOIN users ON followers.seguido_id = users.id
            WHERE followers.seguidor_id = %s;
        """, [self.id])

        seguindo = cur.fetchall()
        cur.close()
        conn.close()

        return [{"id": row[0], "nome": row[1]} for row in seguindo]