from models.base_model import BaseModel
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    __tabela = "users"

    def __init__(self, nome, email, senha, id=None):
        super().__init__()
        self._id = id
        self.__nome = nome
        self.__email = email
        self.__senha_hash = self._gerar_hash_senha(senha) if senha else None

    @property
    def nome(self):
        return self.__nome

    @property
    def email(self):
        return self.__email

    def _gerar_hash_senha(self, senha):
        return generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.__senha_hash, senha)

    def salvar_no_banco(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (nome, email, senha_hash) 
            VALUES (%s, %s, %s) RETURNING id;
        """, [self.nome, self.email, self.__senha_hash])

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
            senha_hash = self._gerar_hash_senha(senha)
            dados["senha_hash"] = senha_hash
            self.__senha_hash = senha_hash
        if dados:
            self.atualizar_dados(**dados)

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