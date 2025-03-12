from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.message import Message
from app.models.notification import Notification
from app.models.community import Group, Event
from app.models.follow_control import FollowControl
from app.security.permission_manager import verificar_autenticacao

crud_bp = Blueprint("crud", __name__)

MODELS = {
    "user": User,
    "post": Post,
    "comment": Comment,
    "like": Like,
    "message": Message,
    "notification": Notification,
    "group": Group,
    "event": Event,
}
TABLES = {
    "user": "users",
    "post": "posts",
    "comment": "comments",
    "like": "likes",
    "message": "messages",
    "follow": "followers",
    "follow_request": "follow_requests",
    "group": "groups",
    "event": "events",
    "notification": "notifications"
}
from flask import Blueprint, request, jsonify
from app.models import MODELS
from app.security.permission_manager import verificar_autenticacao

crud_bp = Blueprint("crud", __name__)

@crud_bp.route("/create/<objeto>", methods=["POST"])
def criar_objeto(objeto):
    """Criação de objetos no banco de dados, garantindo segurança e permissões"""

    # 🔹 **Valida o token do usuário**
    usuario_id, erro = verificar_autenticacao(request)
    if erro:
        return erro  # Retorna erro 401 se não estiver autenticado

    if objeto not in MODELS:
        return jsonify({"erro": "Tipo de objeto inválido!"}), 400

    data = request.json  # Dados enviados pelo cliente
    ModelClass = MODELS[objeto]  # Obtém a classe do modelo correspondente

    try:
        # 🔹 **VERIFICAÇÃO DE REGRAS ESPECÍFICAS POR TIPO DE OBJETO** 🔹
        if objeto = "user":
            return jsonify({"erro": "Criação de usuários não permitida por este endpoint"}), 403
        else:
            data["user_id"] = usuario_id

       

        # 🔹 **Cria o objeto no banco** 🔹
        novo_objeto = ModelClass(**data)
        novo_objeto.salvar_no_banco()

        return jsonify({"mensagem": f"{objeto.capitalize()} criado com sucesso!", "id": novo_objeto.id}), 201

    except Exception as e:
        return jsonify({"erro": f"Erro ao criar {objeto}: {str(e)}"}), 500

     
@crud_bp.route("/get/<objeto>/<int:objeto_id>", methods=["GET"])
def get_objeto(objeto, objeto_id):
    if objeto not in MODELS:
        return jsonify({"erro": "Objeto inválido"}), 400

    ModelClass = MODELS[objeto]  # Obtém a classe correta
    objeto_encontrado = ModelClass.buscar_por_id(objeto_id)  

    if not objeto_encontrado:
        return jsonify({"erro": f"{objeto.capitalize()} não encontrado!"}), 404

    return jsonify(objeto_encontrado), 200  


@crud_bp.route("/edit/<objeto>/<id>", methods=["PUT"])
def editar_objeto(objeto, id):
    """Atualiza um objeto existente no banco de dados."""
    if objeto not in MODELS:
        return jsonify({"erro": "Tipo de objeto inválido!"}), 400

    data = request.json  # Dados enviados pelo cliente
    ModelClass = MODELS[objeto]  # Obtém a classe do modelo correspondente

    try:
        objeto_encontrado = ModelClass.buscar_por_id(cls=ModelClass, objeto_id=id)  # Busca o objeto no banco
        if not objeto_encontrado:
            return jsonify({"erro": f"{objeto.capitalize()} não encontrado!"}), 404

        # Atualiza os dados do objeto usando o método de atualização do Model
        objeto_encontrado.atualizar_dados(**data)

        return jsonify({"mensagem": f"{objeto.capitalize()} atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar {objeto}: {str(e)}"}), 500


@crud_bp.route("/delete/<objeto>/<id>", methods=["DELETE"])
def deletar_objeto(objeto, id):
    """Deleta um objeto do banco de dados pelo ID."""
    if objeto not in MODELS:
        return jsonify({"erro": "Tipo de objeto inválido!"}), 400

    ModelClass = MODELS[objeto]  # Obtém a classe correspondente

    try:
        objeto_encontrado = ModelClass.buscar_por_id(id)  # Busca o objeto no banco
        if not objeto_encontrado:
            return jsonify({"erro": f"{objeto.capitalize()} não encontrado!"}), 404

        objeto_encontrado.deletar_do_banco()  # Remove o objeto do banco
        return jsonify({"mensagem": f"{objeto.capitalize()} deletado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar {objeto}: {str(e)}"}), 500