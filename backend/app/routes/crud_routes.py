from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.message import Message
from app.models.notification import Notification
from app.models.community import Group, Event
from app.models.follow_control import FollowControl

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
    "follow": FollowControl
}

@crud_bp.route("/create/<objeto>", methods=["POST"])
def criar_objeto(objeto):
    """Cria um novo objeto no banco de dados, baseado no tipo informado na URL."""
    if objeto not in MODELS:
        return jsonify({"erro": "Tipo de objeto inválido!"}), 400

    data = request.json  # Recebe os dados enviados na requisição
    ModelClass = MODELS[objeto]  # Pega a classe correta do dicionário MODELS

    try:
        novo_obj = ModelClass(**data)  # Cria a instância do objeto
        novo_obj.salvar_no_banco()  # Salva no banco de dados
        return jsonify({"mensagem": f"{objeto.capitalize()} criado com sucesso!", "id": novo_obj.id}), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar {objeto}: {str(e)}"}), 500

     
@crud_bp.route("/get/<objeto>/<id>", methods=["GET"])
def buscar_objeto(objeto, id):
    """Busca um objeto no banco de dados pelo ID."""
    if objeto not in MODELS:
        return jsonify({"erro": f"Tipo de objeto inválido!"}), 400

    ModelClass = MODELS[objeto]  # Obtém a classe do modelo correspondente
    try:
        objeto_encontrado = ModelClass.buscar_por_id(id)  # Método genérico de busca no Model
        if not objeto_encontrado:
            return jsonify({"erro": f"{objeto.capitalize()} não encontrado!"}), 404

        return jsonify(objeto_encontrado.exibir_info()), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar {objeto}: {str(e)}"}), 500


@crud_bp.route("/edit/<objeto>/<id>", methods=["PUT"])
def editar_objeto(objeto, id):
    """Atualiza um objeto existente no banco de dados."""
    if objeto not in MODELS:
        return jsonify({"erro": "Tipo de objeto inválido!"}), 400

    data = request.json  # Dados enviados pelo cliente
    ModelClass = MODELS[objeto]  # Obtém a classe do modelo correspondente

    try:
        objeto_encontrado = ModelClass.buscar_por_id(id)  # Busca o objeto no banco
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