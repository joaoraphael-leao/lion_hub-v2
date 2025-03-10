from database import get_db_connection

class FollowControl:
    @staticmethod
    def seguir_usuario(seguidor_id, seguido_id):
        """Segue um usuário (apenas perfis públicos)."""
        if seguidor_id == seguido_id:
            return {"erro": "Você não pode seguir a si mesmo."}

        conn = get_db_connection()
        cur = conn.cursor()

        # Verifica se o perfil é privado
        cur.execute("SELECT privacidade FROM users WHERE id = %s", [seguido_id])
        resultado = cur.fetchone()

        if resultado and not resultado[0]:  # Se privacidade = False (perfil privado)
            return FollowControl.pedir_para_seguir(seguidor_id, seguido_id)

        try:
            cur.execute("""
                INSERT INTO followers (seguidor_id, seguido_id)
                VALUES (%s, %s)
                ON CONFLICT (seguidor_id, seguido_id) DO NOTHING;
            """, [seguidor_id, seguido_id])
            conn.commit()
            return {"mensagem": "Agora você está seguindo esse usuário."}
        except Exception as e:
            return {"erro": str(e)}
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def pedir_para_seguir(seguidor_id, seguido_id):
        """Cria um pedido de seguimento para perfis privados."""
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO follow_requests (seguidor_id, seguido_id)
                VALUES (%s, %s)
                ON CONFLICT (seguidor_id, seguido_id) DO NOTHING;
            """, [seguidor_id, seguido_id])
            conn.commit()
            return {"mensagem": "Pedido de seguimento enviado."}
        except Exception as e:
            return {"erro": str(e)}
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def aceitar_pedido(seguidor_id, seguido_id):
        """Aceita um pedido de seguimento."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM follow_requests WHERE seguidor_id = %s AND seguido_id = %s;
        """, [seguidor_id, seguido_id])

        cur.execute("""
            INSERT INTO followers (seguidor_id, seguido_id)
            VALUES (%s, %s)
            ON CONFLICT (seguidor_id, seguido_id) DO NOTHING;
        """, [seguidor_id, seguido_id])
        conn.commit()

        cur.close()
        conn.close()
        return {"mensagem": "Pedido de seguimento aceito."}

    @staticmethod
    def recusar_pedido(seguidor_id, seguido_id):
        """Recusa um pedido de seguimento."""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM follow_requests WHERE seguidor_id = %s AND seguido_id = %s;
        """, [seguidor_id, seguido_id])
        conn.commit()

        cur.close()
        conn.close()
        return {"mensagem": "Pedido de seguimento recusado."}