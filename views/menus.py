# views/menus.py

from controllers import account_controller, post_controller, event_controller, group_controller
from storage import users

def main_menu():
    while True:
        print("\nBem-vindo à Rede Social!")
        print("1) Criar Conta")
        print("2) Login")
        print("3) Sair")
        option = input("Escolha uma opção: ")
        if option == '1':
            user = account_controller.create_user()
            if user:
                user_menu(user)
        elif option == '2':
            user = account_controller.login()
            if user:
                user_menu(user)
        elif option == '3':
            break
        else:
            print("Opção inválida.")

def user_menu(user):
    while True:
        if not user.isActive():
            print("Sua conta foi desativada. Voltando ao menu principal.")
            break
        print(f"\nBem-vindo, {user.getName()}!")
        print("1) Menu de Posts")
        print("2) Menu da Conta")
        print("3) Menu de Notificações")
        print("4) Menu Social")
        print("5) Menu de Eventos")
        print("6) Menu de Grupos")
        print("7) Logout")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            post_controller.create_post(user)
        elif choice == '2':
            account_controller.edit_account(user)
        elif choice == '3':
            # Exibe notificações
            for notif in user.getNotifications():
                print(notif.get("message", ""))
            input("Pressione Enter para continuar...")
        elif choice == '4':
            social_menu(user)
        elif choice == '5':
            event_controller.create_event(user)
        elif choice == '6':
            group_controller.create_group(user)
        elif choice == '7':
            break
        else:
            print("Opção inválida.")

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