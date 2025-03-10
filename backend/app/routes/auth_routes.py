import jwt
import datetime
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.database import get_db_connection
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)
SECRET_KEY = "minha_chave_secreta"  # 🔐 Trocar por uma chave segura

revoked_tokens = set()  # 🔹 Lista de tokens revogados

# 🔹 Rota de Login
@auth_bp.route("/login", methods=["POST"])
def login():
    """Autentica um usuário e retorna um token JWT."""
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    # 🔍 Busca usuário no banco
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, senha FROM users WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    if not usuario or not check_password_hash(usuario[1], senha):
        return jsonify({"erro": "Email ou senha inválidos!"}), 401

    # 🔐 Gerando token JWT válido por 24 horas
    token = jwt.encode(
        {"id": usuario[0], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token}), 200

# 🔹 Função para obter usuário logado
def get_usuario_logado():
    """Decodifica o token JWT para obter o usuário logado, garantindo que ele não foi revogado."""
    token = request.headers.get("Authorization")

    if not token or token in revoked_tokens:
        return None  

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["id"]
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

# 🔹 Rota de Logout
@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Revoga o token atual do usuário."""
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"erro": "Nenhum token fornecido!"}), 400

    revoked_tokens.add(token)  # 🔹 Armazena o token como revogado
    return jsonify({"mensagem": "Logout realizado com sucesso!"}), 200

# 🔹 Rota de Renovação de Token
@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Renova o token JWT se ele ainda for válido."""
    token = request.headers.get("Authorization")

    if not token or token in revoked_tokens:
        return jsonify({"erro": "Token inválido ou revogado!"}), 403

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        novo_token = jwt.encode(
            {"id": decoded["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": novo_token}), 200
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido!"}), 403