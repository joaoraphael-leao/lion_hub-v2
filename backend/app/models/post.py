from models.base_model import BaseModel
from database import get_db_connection

class Post(BaseModel):
    __tabela = "posts"

    def __init__(self, autor_id, titulo, descricao, midia=None, id=None):
        super().__init__()
        self._id = id
        self.__autor_id = autor_id
        self.__titulo = titulo
        self.__descricao = descricao
        self.__midia = midia

    @property
    def autor_id(self):
        return self.__autor_id

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
            INSERT INTO posts (autor_id, titulo, descricao, midia)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (self.autor_id, self.titulo, self.descricao, self.midia))

        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    def atualizar_post(self, titulo=None, descricao=None, midia=None):
        dados = {}

        if titulo:
            dados["titulo"] = titulo
            self.__titulo = titulo

        if descricao:
            dados["descricao"] = descricao
            self.__descricao = descricao

        if midia:
            dados["midia"] = midia
            self.__midia = midia

        if dados:
            self.atualizar_dados(**dados)

    def exibir_info(self):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT nome FROM users WHERE id = %s;
    """, [self.autor_id])  

    autor = cur.fetchone()

    cur.close()
    conn.close()

    if autor:
        return {
            "post_id": self.id,
            "autor": autor[0],
            "titulo": self.titulo,
            "descricao": self.descricao,
            "midia": self.midia
        }
    else:
        return None