# views/menus.py

from controllers import account_controller, post_controller, event_controller, group_controller
from storage import users

def follow_user(user):
    print("Usuários disponíveis para seguir:")
    for u in users:
        if u != user and u.isActive():
            print(f"{u.getId()} - {u.getName()}")
    try:
        uid = int(input("Digite o ID do usuário para seguir: "))
    except ValueError:
        print("ID inválido.")
        return
    target = next((u for u in users if u.getId() == uid), None)
    if target:
        if target._privacity:
            target.addNotification({
                "user": user,
                "message": f"{user.getName()} solicitou para te seguir.",
                "is_follow_notification": True,
                "follow_request": True
            })
            print("Solicitação enviada.")
        else:
            user.follow(target)
            target.addNotification({
                "user": user,
                "message": f"{user.getName()} começou a te seguir.",
                "is_follow_notification": True
            })
            print(f"Você começou a seguir {target.getName()}.")
    else:
        print("Usuário não encontrado.")



def send_message(user):
    print("Usuários disponíveis para enviar mensagem:")
    for u in users:
        if u != user and u.isActive():
            print(f"{u.getId()} - {u.getName()}")
    try:
        uid = int(input("Digite o ID do usuário para enviar mensagem: "))
    except ValueError:
        print("ID inválido.")
        return
    target = next((u for u in users if u.getId() == uid), None)
    if target:
        message = input("Digite sua mensagem: ")
        target.addNotification({
            "user": user,
            "message": message,
            "is_message": True
        })
        print("Mensagem enviada!")
    else:
        print("Usuário não encontrado.")

def posts_menu(my_user):
    while True:
        print("Menu de Posts:")
        print("1) Criar Post")
        print("2) Editar Post")
        print("3) Deletar algum Post")
        print("4) Ver todos os posts")
        print("5) Pesquisar posts")
        print("6) Voltar")
        choice = input("Escolha uma das opções acima: ")
        if choice == '1':
            post_controller.create_post(my_user)
        elif choice == '2':
            post_controller.edit_post(my_user)
        elif choice == '3':
            post_controller.delete_post(my_user)
        elif choice == '4':
            post_controller.see_all_posts(my_user)
        elif choice == '5':
            post_controller.search_posts(my_user)
        elif choice == '6':
            break
        else:
            print("Opção inválida!")

def group_menu(current_user):
    while True:
        print("\nMenu de Grupos:")
        print("1) Criar Grupo")
        print("2) Listar Grupos")
        print("3) Gerenciar Meus Grupos")
        print("4) Voltar")
        op = input("Escolha uma opção: ")
        if op == '1':
            group_controller.create_group(current_user)
        elif op == '2':
            group_controller.list_groups()
        elif op == '3':
            group_controller.manage_group(current_user)
        elif op == '4':
            break
        else:
            print("Opção inválida!")

def account_menu(my_user):
    while True:
        print("Menu da Conta:")
        print("1) Editar dados da conta")
        print("2) Deletar Conta")
        print("3) Voltar")
        choice = input("Escolha uma das opções acima: ")
        if choice == '1':
            account_controller.edit_account(my_user)
        elif choice == '2':
            account_controller.delete_account(my_user)
            return
        elif choice == '3':
            break
        else:
            print("Opção inválida!")

def notifications_menu(my_user):
    while True:
        print("Menu de Notificações:")
        print("1) Ver todas as notificações")
        print("2) Voltar")
        choice = input("Escolha uma das opções acima: ")
        if choice == '1':
            notifications = my_user.getNotifications()
            for notif in notifications:
                print(notif["message"])
        elif choice == '2':
            break
        else:
            print("Opção inválida!")

def social_menu(my_user):
    while True:
        print("Menu Social:")
        print("1) Seguir novas pessoas")
        print("2) Ver usuários")
        print("3) Enviar mensagens para alguém")
        print("4) Voltar")
        choice = input("Escolha uma das opções acima: ")
        if choice == '1':
            my_user.follow_someone()
        elif choice == '2':
            account_controller.show_users(my_user)
        elif choice == '3':
            send_message(my_user)
        elif choice == '4':
            break
        else:
            print("Opção inválida!")

def events_menu(current_user):
    while True:
        print("\nMenu de Eventos:")
        print("1) Criar Evento")
        print("2) Convidar Pessoas para Evento")
        print("3) Listar Eventos")
        print("4) Ver detalhes do Evento")
        print("5) Voltar")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            event_controller.create_event(current_user)
        elif choice == '2':
            event_controller.invite_to_event(current_user)
        elif choice == '3':
            event_controller.list_events()
        elif choice == '4':
            event_controller.show_event_details()
        elif choice == '5':
            break
        else:
            print("Opção inválida!")

def user_options_menu(my_user):
    while True:
        if my_user._active == False:
            print("Sua conta foi desativada. Você será redirecionado para a tela de login.")
            break
        print("\nOpções de Usuário:")
        print("1) Menu de Posts")
        print("2) Menu da Conta")
        print("3) Menu de Notificações")
        print("4) Menu Social")
        print("5) Menu de Eventos")
        print("6) Menu de Grupos")
        print("7) Sair")
        user_choice = input("Escolha uma das opções: ")
        if user_choice == '1':
            posts_menu(my_user)
        elif user_choice == '2':
            account_menu(my_user)
        elif user_choice == '3':
            notifications_menu(my_user)
        elif user_choice == '4':
            social_menu(my_user)
        elif user_choice == '5':
            events_menu(my_user)
        elif user_choice == '6':
            group_menu(my_user)
        elif user_choice == '7':
            break
        else:
            print("Opção inválida!")

def social_menu(user):
    while True:
        print("\nMenu Social:")
        print("1) Seguir Usuário")
        print("2) Enviar Mensagem")
        print("3) Ver Usuários")
        print("4) Voltar")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            follow_user(user)
        elif choice == '2':
            send_message(user)
        elif choice == '3':
            for u in users:
                if u != user and u.isActive():
                    print(f"{u.getId()} - {u.getName()}")
            input("Pressione Enter para voltar...")
        elif choice == '4':
            break
        else:
            print("Opção inválida.")

def general_menu():
    option = ""
    while option != '3':
        option = input("""
        Bem-vindo à rede social!
        1) Criar conta
        2) Login
        3) Sair
        Escolha uma opção: """)
        if option == '1':
            my_user = account_controller.create_user()
            user_options_menu(my_user)
        elif option == '2':
            userEmail = input("Digite seu email: ")
            userPassword = input("Digite sua senha: ")
            my_user = next(
                (user for user in users if user.getEmail() == userEmail and user.getPassword() == userPassword), None)
            if not my_user:
                print("Email ou senha incorretos!")
                continue
            user_options_menu(my_user)
        elif option != '3':
            print("Opção inválida!")


