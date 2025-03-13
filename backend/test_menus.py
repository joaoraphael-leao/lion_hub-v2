import unittest
from unittest.mock import patch
import io
import sys
import main  # Supondo que o arquivo main.py esteja no mesmo diretório

# Classes Dummy para simular o comportamento dos modelos

class DummyUser:
    def __init__(self, id=1, nome='TestUser', email='test@example.com', senha='password'):
        self.id = id
        self.__nome = nome
        self.__email = email
        self.__senha = senha

    @property
    def nome(self):
        return self.__nome

    def verificar_senha(self, senha):
        return senha == self.__senha

    def exibir_info(self):
        return {"id": self.id, "nome": self.__nome, "email": self.__email, "seguidores": 10}

    def atualizar_usuario(self, nome, senha):
        if nome:
            self.__nome = nome
        if senha:
            self.__senha = senha

    def deletar_do_banco(self):
        pass

    def ver_seguidores(self):
        return [{"id": 2, "nome": "Follower"}]

    def ver_seguindo(self):
        return [{"id": 3, "nome": "Following"}]

    def tornar_publico(self):
        pass

    def tornar_privado(self):
        pass

class DummyPost:
    def __init__(self, user_id=1, titulo='Titulo', descricao='Descricao', midia='', id=1):
        self.id = id
        self.__user_id = user_id
        self.__titulo = titulo
        self.__descricao = descricao
        self.__midia = midia

    def salvar_no_banco(self):
        pass

    @staticmethod
    def buscar_por_id(post_id):
        if post_id == "1":
            return {"id": 1, "user_id": 1, "titulo": "Titulo", "descricao": "Descricao", "midia": ""}
        return None

    @staticmethod
    def deletar_post(post_id):
        if post_id == "1":
            return {"mensagem": "Post deletado com sucesso"}
        return {"erro": "Post não encontrado"}

class DummyComment:
    @staticmethod
    def buscar_por_post(post_id):
        return [{"id": 1, "autor_id": 1, "autor_nome": "TestUser", "conteudo": "Comentario", "data": "2020-01-01"}]

    @staticmethod
    def deletar_comentario(comentario_id, user_id):
        if comentario_id == "1":
            return {"mensagem": "Comentario deletado com sucesso"}
        return {"erro": "Comentario não encontrado"}

class DummyLike:
    @staticmethod
    def contar_curtidas(identifier):
        return 5

class DummyFollowControl:
    @staticmethod
    def seguir_usuario(user_id, seguido_id):
        if user_id == seguido_id:
            return {"erro": "Você não pode seguir a si mesmo."}
        return {"mensagem": "Agora você está seguindo esse usuário."}

    @staticmethod
    def deixar_de_seguir(user_id, seguido_id):
        return {"mensagem": "Você deixou de seguir esse usuário."}

class DummyMessage:
    def __init__(self, remetente_id, destinatario_id, conteudo, id=1):
        self.remetente_id = remetente_id
        self.destinatario_id = destinatario_id
        self.conteudo = conteudo

    def salvar_no_banco(self):
        pass

    @staticmethod
    def buscar_historico(remetente_id, destinatario_id, usuario_id):
        return [{"id": 1, "remetente_id": remetente_id, "destinatario_id": destinatario_id, "conteudo": "Hello", "data_criacao": "2020-01-01"}]

class DummyNotification:
    @staticmethod
    def buscar_notificacoes(usuario_id):
        return [{"id": 1, "tipo": "like", "objeto_id": 1, "lida": False}]

class DummyGroup:
    @staticmethod
    def buscar_por_usuario(user_id):
        return [{"id": 1, "owner_id": user_id, "nome": "Grupo1", "descricao": "Descricao", "privacidade": True}]

    def salvar_no_banco(self):
        pass

class DummyEvent:
    @staticmethod
    def buscar_por_usuario(user_id):
        return [{"id": 1, "owner_id": user_id, "nome": "Evento1", "descricao": "Descricao", "data": "2020-01-01", "localizacao": "Local", "privacidade": True}]

    def salvar_no_banco(self):
        pass

# Testes para os menus

class TestMenus(unittest.TestCase):

    def setUp(self):
        main.usuario_logado = DummyUser()

        # Patches para os métodos dos modelos
        self.patcher_user_salvar = patch('main.User.salvar_no_banco', lambda self: None)
        self.patcher_user_buscar = patch('main.User.buscar_por_email', return_value=DummyUser())
        self.patcher_post_buscar = patch('main.Post.buscar_por_id', side_effect=DummyPost.buscar_por_id)
        self.patcher_post_deletar = patch('main.Post.deletar_post', side_effect=DummyPost.deletar_post)
        self.patcher_comment_buscar = patch('main.Comment.buscar_por_post', side_effect=DummyComment.buscar_por_post)
        self.patcher_comment_deletar = patch('main.Comment.deletar_comentario', side_effect=DummyComment.deletar_comentario)
        self.patcher_like_contar = patch('main.Like.contar_curtidas', side_effect=DummyLike.contar_curtidas)
        self.patcher_follow_seguir = patch('main.FollowControl.seguir_usuario', side_effect=DummyFollowControl.seguir_usuario)
        self.patcher_follow_deixar = patch('main.FollowControl.deixar_de_seguir', side_effect=DummyFollowControl.deixar_de_seguir)
        self.patcher_message_buscar = patch('main.Message.buscar_historico', side_effect=DummyMessage.buscar_historico)
        self.patcher_notification_buscar = patch('main.Notification.buscar_notificacoes', side_effect=DummyNotification.buscar_notificacoes)
        self.patcher_group_buscar = patch('main.Group.buscar_por_usuario', side_effect=DummyGroup.buscar_por_usuario)
        self.patcher_event_buscar = patch('main.Event.buscar_por_usuario', side_effect=DummyEvent.buscar_por_usuario)

        self.patcher_user_salvar.start()
        self.patcher_user_buscar.start()
        self.patcher_post_buscar.start()
        self.patcher_post_deletar.start()
        self.patcher_comment_buscar.start()
        self.patcher_comment_deletar.start()
        self.patcher_like_contar.start()
        self.patcher_follow_seguir.start()
        self.patcher_follow_deixar.start()
        self.patcher_message_buscar.start()
        self.patcher_notification_buscar.start()
        self.patcher_group_buscar.start()
        self.patcher_event_buscar.start()

    def tearDown(self):
        patch.stopall()

    def test_menu_inicial_register_and_exit(self):
        inputs = iter([
            '1',         # Registrar usuário
            'TestUser',
            'test@example.com',
            'password',
            '3'          # Sair
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_inicial()
            output = buf.getvalue()
            self.assertIn("Usuário registrado com sucesso", output)

    def test_menu_inicial_login_and_logout(self):
        inputs = iter([
            '2',         # Login
            'test@example.com',
            'password',
            '10',        # Logout no menu principal
            '3'          # Sair do menu_inicial após logout
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_inicial()
            output = buf.getvalue()
            self.assertIn("Bem-vindo", output)
            self.assertIn("Você foi deslogado com sucesso", output)

    def test_menu_usuarios_options(self):
        inputs = iter([
            '1',   # Ver Perfil
            '2',   # Atualizar Nome/Senha (entradas vazias)
            '',
            '',
            '3',   # Alterar Privacidade (tornar público)
            's',
            '4',   # Desativar Conta
            's',   # Confirma desativação
            '3'    # Sair do menu_inicial após desativação
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_usuarios()
            output = buf.getvalue()
            self.assertIn("Informações atualizadas", output)
            self.assertIn("Privacidade atualizada", output)
            self.assertIn("Conta desativada com sucesso", output)

    def test_menu_posts_options(self):
        inputs = iter([
            '1',           # Criar Post
            'Novo Post',   # Título
            'Descrição',   # Descrição
            '',            # Mídia (opcional)
            '2',           # Ver Post
            '1',           # ID do post
            '3',           # Ver Estatísticas do Post
            '1',           # ID do post para estatísticas
            '4',           # Editar Post
            '1',           # ID do post
            'Editado',     # Novo título
            'Editado desc',# Nova descrição
            '',            # Nova mídia
            '5',           # Deletar Post
            '1',           # ID do post para deletar
            '6'            # Voltar
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_posts()
            output = buf.getvalue()
            self.assertIn("Post criado com sucesso", output)
            self.assertIn("Curtidas", output)
            self.assertIn("Post deletado com sucesso", output)

    def test_menu_comentarios_options(self):
        inputs = iter([
            '1',  # Criar Comentário
            '1',  # ID do post
            'Um comentário',
            '2',  # Ver Comentários
            '1',  # ID do post para ver comentários
            '3',  # Deletar Comentário
            '1',  # ID do comentário
            '4'   # Voltar
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_comentarios()
            output = buf.getvalue()
            self.assertIn("Comentário criado", output)
            self.assertIn("Comentario", output)
            self.assertIn("Comentario deletado com sucesso", output)

    def test_menu_likes_options(self):
        with io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_likes()
            output = buf.getvalue()
            self.assertIn("Total de curtidas", output)

    def test_menu_seguidores_options(self):
        inputs = iter([
            '1',   # Ver Seguidores
            '2',   # Ver Seguindo
            '3',   # Seguir Usuário
            '2',   # ID do usuário a seguir
            '4',   # Deixar de Seguir
            '2',   # ID do usuário a deixar de seguir
            '5'    # Voltar
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_seguidores()
            output = buf.getvalue()
            self.assertIn("Seguidores:", output)
            self.assertIn("Seguindo:", output)
            self.assertIn("Agora você está seguindo", output)
            self.assertIn("deixar de seguir", output)

    def test_menu_mensagens_options(self):
        inputs = iter([
            '1',   # Enviar Mensagem
            '2',   # ID do destinatário
            'Hello',  # Mensagem
            '2',   # Ver Histórico de Mensagens
            '2',   # ID do destinatário para histórico
            '3'    # Voltar
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_mensagens()
            output = buf.getvalue()
            self.assertIn("Mensagem enviada", output)
            self.assertIn("Hello", output)

    def test_menu_notificacoes_options(self):
        with io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_notificacoes()
            output = buf.getvalue()
            self.assertIn("like", output)

    def test_menu_grupos_options(self):
        inputs = iter([
            '1',   # Criar Grupo
            'GrupoTeste',
            'DescricaoTeste',
            '2',   # Ver Meus Grupos
            '3',   # Convidar Usuário para Grupo
            '1',   # ID do grupo
            '2',   # ID do usuário a convidar
            '4'    # Voltar
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_grupos()
            output = buf.getvalue()
            self.assertIn("Grupo criado com sucesso", output)
            self.assertIn("convidado para o grupo", output)

    def test_menu_eventos_options(self):
        inputs = iter([
            '1',   # Criar Evento
            'EventoTeste',
            'DescricaoTeste',
            '2025-03-14',
            'LocalTeste',
            '2',   # Ver Meus Eventos
            '3',   # Convidar Usuário para Evento
            '1',   # ID do evento
            '2',   # ID do usuário a convidar
            '4'    # Voltar
        ])
        with patch('builtins.input', lambda _: next(inputs)), io.StringIO() as buf, patch('sys.stdout', buf):
            main.menu_eventos()
            output = buf.getvalue()
            self.assertIn("Evento criado com sucesso", output)
            self.assertIn("convidado para o evento", output)

if __name__ == '__main__':
    unittest.main()