from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.follow_control import FollowControl
from app.models.message import Message
from app.models.notification import Notification
from app.models.community import Group, Event

usuario_logado = None  # Armazena o usuário autenticado

def menu_inicial():
    global usuario_logado
    while True:
        print("\n🔐 MENU INICIAL")
        print("1️⃣ - Registrar Usuário")
        print("2️⃣ - Login")
        print("3️⃣ - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("E-mail: ")
            senha = input("Senha: ")
            usuario = User(nome, email, senha)
            usuario.salvar_no_banco()
            print("✅ Usuário registrado com sucesso!")

        elif opcao == "2":
            email = input("E-mail: ")
            senha = input("Senha: ")
            usuario_logado = User.buscar_por_email(email)
            if usuario_logado and usuario_logado.verificar_senha(senha):
                print(f"✅ Bem-vindo, {usuario_logado.nome}!")
                menu_principal()
            else:
                print("❌ Email ou senha incorretos.")
                usuario_logado = None

        elif opcao == "3":
            print("👋 Saindo do sistema...")
            break

def menu_principal():
    global usuario_logado
    while True:
        print("\n🌍 MENU PRINCIPAL")
        print("1️⃣ - Gerenciar Usuários")
        print("2️⃣ - Gerenciar Posts")
        print("3️⃣ - Gerenciar Comentários")
        print("4️⃣ - Gerenciar Likes")
        print("5️⃣ - Gerenciar Seguidores")
        print("6️⃣ - Gerenciar Mensagens")
        print("7️⃣ - Gerenciar Notificações")
        print("8️⃣ - Gerenciar Grupos")
        print("9️⃣ - Gerenciar Eventos")
        print("🔟 - Logout")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_usuarios()
        elif opcao == "2":
            menu_posts()
        elif opcao == "3":
            menu_comentarios()
        elif opcao == "4":
            menu_likes()
        elif opcao == "5":
            menu_seguidores()
        elif opcao == "6":
            menu_mensagens()
        elif opcao == "7":
            menu_notificacoes()
        elif opcao == "8":
            menu_grupos()
        elif opcao == "9":
            menu_eventos()
        elif opcao == "10":
            print("👋 Você foi deslogado com sucesso!")
            usuario_logado = None
            menu_inicial()
            break

def menu_usuarios():
    global usuario_logado
    while True:
        print("\n👤 MENU USUÁRIOS")
        print("1️⃣ - Ver Perfil")
        print("2️⃣ - Atualizar Nome/Senha")
        print("3️⃣ - Alterar Privacidade")
        print("4️⃣ - Desativar Conta")
        print("5️⃣ - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                info = usuario_logado.exibir_info()
                print(info)
            except Exception as e:
                print(f"❌ Erro ao exibir perfil: {e}")

        elif opcao == "2":
            try:
                nome = input("Novo nome (deixe em branco para manter): ")
                senha = input("Nova senha (deixe em branco para manter): ")
                usuario_logado.atualizar_usuario(nome if nome else None, senha if senha else None)
                print("✅ Informações atualizadas!")
            except Exception as e:
                print(f"❌ Erro ao atualizar informações: {e}")

        elif opcao == "3":
            try:
                privacidade = input("Tornar perfil público? (s/n): ")
                if privacidade.lower() == "s":
                    usuario_logado.tornar_publico()
                else:
                    usuario_logado.tornar_privado()
                print("✅ Privacidade atualizada!")
            except Exception as e:
                print(f"❌ Erro ao alterar privacidade: {e}")

        elif opcao == "4":
            try:
                confirmacao = input("Tem certeza que deseja desativar sua conta? (s/n): ")
                if confirmacao.lower() == "s":
                    usuario_logado.deletar_do_banco(tabela="users")
                    print("✅ Conta desativada com sucesso!")
                    usuario_logado = None
                    menu_inicial()
                    break
            except Exception as e:
                print(f"❌ Erro ao desativar conta: {e}")

        elif opcao == "5":
            break

def menu_posts():
    while True:
        print("\n📝 MENU POSTS")
        print("1️⃣ - Criar Post")
        print("2️⃣ - Ver Post")
        print("3️⃣ - Ver Estatísticas do Post")
        print("4️⃣ - Editar Post")
        print("5️⃣ - Deletar Post")
        print("6️⃣ - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                titulo = input("Título do post: ")
                descricao = input("Descrição: ")
                midia = input("Mídia (opcional): ")
                post = Post(usuario_logado.id, titulo, descricao, midia)
                post.salvar_no_banco()
                print("✅ Post criado com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao criar post: {e}")

        elif opcao == "2":
            try:
                post_id = input("ID do post: ")
                post_data = Post.buscar_por_id(post_id, "posts")
                if post_data:
                    print(post_data)
                else:
                    print("❌ Post não encontrado.")
            except Exception as e:
                print(f"❌ Erro ao buscar post: {e}")

        elif opcao == "3":
            try:
                post_id = input("ID do post: ")
                curtidas = Like.contar_curtidas(post_id)
                comentarios = Comment.buscar_por_post(post_id)
                print(f"👍 Curtidas: {curtidas}")
                print(f"💬 Comentários: {len(comentarios)}")
            except Exception as e:
                print(f"❌ Erro ao buscar estatísticas: {e}")

        elif opcao == "4":
            try:
                post_id = input("ID do post: ")
                titulo = input("Novo título: ")
                descricao = input("Nova descrição: ")
                midia = input("Nova mídia: ")
                post_data = Post.buscar_por_id(post_id, "posts")
                if post_data:
                    # Para atualização, criamos uma instância e chamamos o método herdado da base
                    post = Post(post_data['user_id'], titulo, descricao, midia, id=post_data['id'])
                    post.atualizar_dados("posts", titulo=titulo, descricao=descricao, midia=midia)
                    print("✅ Post atualizado com sucesso!")
                else:
                    print("❌ Post não encontrado.")
            except Exception as e:
                print(f"❌ Erro ao atualizar post: {e}")

        elif opcao == "5":
            try:
                post_id = input("ID do post: ")
                resposta = Post.deletar_post(post_id)
                print(resposta.get("mensagem", resposta.get("erro")))
            except Exception as e:
                print(f"❌ Erro ao deletar post: {e}")

        elif opcao == "6":
            break

def menu_comentarios():
    while True:
        print("\n📌 MENU COMENTÁRIOS")
        print("1️⃣ - Criar Comentário")
        print("2️⃣ - Ver Comentários")
        print("3️⃣ - Deletar Comentário")
        print("4️⃣ - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                post_id = input("ID do post: ")
                conteudo = input("Digite o comentário: ")
                comentario = Comment(post_id, usuario_logado.id, conteudo)
                comentario.salvar_no_banco()
                print("✅ Comentário criado!")
            except Exception as e:
                print(f"❌ Erro ao criar comentário: {e}")

        elif opcao == "2":
            try:
                post_id = input("ID do post: ")
                comentarios = Comment.buscar_por_post(post_id)
                for c in comentarios:
                    print(f"{c['autor_id']} - {c.get('autor_nome', '')}: {c['conteudo']} ({c['data']})")
            except Exception as e:
                print(f"❌ Erro ao buscar comentários: {e}")

        elif opcao == "3":
            try:
                comentario_id = input("ID do comentário: ")
                resposta = Comment.deletar_comentario(comentario_id, usuario_logado.id)
                print(resposta.get("mensagem", resposta.get("erro")))
            except Exception as e:
                print(f"❌ Erro ao deletar comentário: {e}")

        elif opcao == "4":
            break

def menu_likes():
    while True:
        print("\n❤️ MENU LIKES")
        print("1️⃣ - Curtir Post")
        print("2️⃣ - Descurtir Post")
        print("3️⃣ - Ver Total de Curtidas de um Post")
        print("4️⃣ - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                post_id = input("ID do post para curtir: ")
                like = Like(usuario_logado.id, post_id)
                resposta = like.salvar_no_banco()
                print(resposta.get("mensagem", resposta.get("erro")))
            except Exception as e:
                print(f"❌ Erro ao curtir post: {e}")

        elif opcao == "2":
            try:
                post_id = input("ID do post para descurtir: ")
                resposta = Like.descurtir(usuario_logado.id, post_id)
                print(resposta.get("mensagem", resposta.get("erro")))
            except Exception as e:
                print(f"❌ Erro ao descurtir post: {e}")

        elif opcao == "3":
            try:
                post_id = input("ID do post: ")
                total = Like.contar_curtidas(post_id)
                print(f"👍 Total de curtidas: {total}")
            except Exception as e:
                print(f"❌ Erro ao buscar curtidas: {e}")

        elif opcao == "4":
            break

        else:
            print("Opção inválida. Tente novamente.")

def menu_seguidores():
    while True:
        print("\n👥 MENU SEGUIDORES")
        print("1️⃣ - Ver Seguidores")
        print("2️⃣ - Ver Seguindo")
        print("3️⃣ - Seguir Usuário")
        print("4️⃣ - Deixar de Seguir")
        print("5️⃣ - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                seguidores = usuario_logado.ver_seguidores()
                print("Seguidores:", seguidores)
            except Exception as e:
                print(f"❌ Erro ao buscar seguidores: {e}")

        elif opcao == "2":
            try:
                seguindo = usuario_logado.ver_seguindo()
                print("Seguindo:", seguindo)
            except Exception as e:
                print(f"❌ Erro ao buscar seguindo: {e}")

        elif opcao == "3":
            try:
                seguido_id = input("ID do usuário que deseja seguir: ")
                resposta = FollowControl.seguir_usuario(usuario_logado.id, seguido_id)
                print(resposta.get("mensagem", resposta.get("erro")))
            except Exception as e:
                print(f"❌ Erro ao seguir usuário: {e}")

        elif opcao == "4":
            try:
                seguido_id = input("ID do usuário que deseja deixar de seguir: ")
                resposta = FollowControl.deixar_de_seguir(usuario_logado.id, seguido_id)
                print(resposta.get("mensagem", resposta.get("erro")))
            except Exception as e:
                print(f"❌ Erro ao deixar de seguir: {e}")

        elif opcao == "5":
            break

def menu_mensagens():
    while True:
        print("\n✉️ MENU MENSAGENS")
        print("1️⃣ - Enviar Mensagem")
        print("2️⃣ - Ver Histórico de Mensagens")
        print("3️⃣ - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                destinatario = input("ID do destinatário: ")
                conteudo = input("Mensagem: ")
                mensagem = Message(usuario_logado.id, destinatario, conteudo)
                mensagem.salvar_no_banco()
                print("✅ Mensagem enviada!")
            except Exception as e:
                print(f"❌ Erro ao enviar mensagem: {e}")

        elif opcao == "2":
            try:
                destinatario = input("ID do destinatário: ")
                historico = Message.buscar_historico(usuario_logado.id, destinatario, usuario_logado.id)
                if isinstance(historico, list):
                    for msg in historico:
                        print(f"{msg['remetente_id']} -> {msg['destinatario_id']}: {msg['conteudo']} ({msg['data_criacao']})")
                else:
                    print(historico.get("erro", "Erro ao buscar histórico de mensagens."))
            except Exception as e:
                print(f"❌ Erro ao buscar histórico de mensagens: {e}")

        elif opcao == "3":
            break

def menu_notificacoes():
    try:
        notificacoes = Notification.buscar_notificacoes(usuario_logado.id)
        for notif in notificacoes:
            print(notif)
    except Exception as e:
        print(f"❌ Erro ao buscar notificações: {e}")

def menu_grupos():
    while True:
        print("\n👥 MENU GRUPOS")
        print("1️⃣ - Criar Grupo")
        print("2️⃣ - Ver Meus Grupos")
        print("3️⃣ - Convidar Usuário para Grupo")
        print("4️⃣ - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                nome = input("Nome do grupo: ")
                descricao = input("Descrição do grupo: ")
                grupo = Group(usuario_logado.id, nome, descricao)
                print("passou")
                grupo.salvar_no_banco()
                print("✅ Grupo criado com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao criar grupo: {e}")

        elif opcao == "2":
            try:
                grupos = Group.buscar_por_usuario(usuario_logado.id)
                for grupo in grupos:
                    print(grupo)
            except Exception as e:
                print(f"❌ Erro ao buscar grupos: {e}")

        elif opcao == "3":
            try:
                grupo_id = input("ID do grupo: ")
                usuario_id = input("ID do usuário a ser convidado: ")
                # Lógica para convidar usuário para o grupo
                print(f"✅ Usuário {usuario_id} convidado para o grupo {grupo_id}.")
            except Exception as e:
                print(f"❌ Erro ao convidar usuário: {e}")

        elif opcao == "4":
            break

def menu_eventos():
    while True:
        print("\n📅 MENU EVENTOS")
        print("1️⃣ - Criar Evento")
        print("2️⃣ - Ver Meus Eventos")
        print("3️⃣ - Convidar Usuário para Evento")
        print("4️⃣ - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                nome = input("Nome do evento: ")
                descricao = input("Descrição do evento: ")
                data = input("Data do evento (YYYY-MM-DD): ")
                localizacao = input("Localização do evento: ")
                evento = Event(usuario_logado.id, nome, descricao, data, localizacao)
                evento.salvar_no_banco()
                print("✅ Evento criado com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao criar evento: {e}")

        elif opcao == "2":
            try:
                eventos = Event.buscar_por_usuario(usuario_logado.id)
                for evento in eventos:
                    print(evento)
            except Exception as e:
                print(f"❌ Erro ao buscar eventos: {e}")

        elif opcao == "3":
            try:
                evento_id = input("ID do evento: ")
                usuario_id = input("ID do usuário a ser convidado: ")
                # Lógica para convidar usuário para o evento
                print(f"✅ Usuário {usuario_id} convidado para o evento {evento_id}.")
            except Exception as e:
                print(f"❌ Erro ao convidar usuário: {e}")

        elif opcao == "4":
            break

if __name__ == "__main__":
    menu_inicial()