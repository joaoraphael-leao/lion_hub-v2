    # controllers/account_controller.py
from models.user import User
from storage import users, posts

def create_user():
    email = input("Digite seu email: ")
    username = input("Digite seu nome: ")
    # Verifica se o nome já existe
    if any(u.getName() == username for u in users):
        print("Esse nome não está disponível.")
        return None
    password = create_password()
    privacity_option = input("Seu perfil será privado? (y/n): ")
    privacity = True if privacity_option.lower() == 'y' else False
    user = User(username, email, password, privacity)
    users.append(user)
    print(f"Usuário {username} criado com sucesso!")
    return user

def create_password():
    while True:
        password = input("Digite sua senha: ")
        confirmPassword = input("Confirme sua senha: ")
        if password == confirmPassword:
            return password
        print("Senhas não conferem! Tente novamente.")

def login():
    email = input("Digite seu email: ")
    password = input("Digite sua senha: ")
    for user in users:
        if user.getEmail() == email and user.getPassword() == password and user.isActive():
            return user
    print("Email ou senha incorretos!")
    return None

def edit_account(user):
    while True:
        print("\nOpções de edição:")
        print("1) Editar Nome")
        print("2) Editar Email")
        print("3) Editar Senha")
        print("4) Voltar")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            new_name = input("Digite o novo nome: ")
            user.setName(new_name)
            print("Nome alterado com sucesso!")
        elif choice == '2':
            new_email = input("Digite o novo email: ")
            user.setEmail(new_email)
            print("Email alterado com sucesso!")
        elif choice == '3':
            new_password = create_password()
            user.setPassword(new_password)
            print("Senha alterada com sucesso!")
        elif choice == '4':
            break
        else:
            print("Opção inválida!")

def delete_account(user):
    # Remove os posts do usuário
    posts_to_remove = [post for post in posts if post.getAuthor() == user]
    for post in posts_to_remove:
        posts.remove(post)
    user.deleteAccount()
    print("Conta desativada com sucesso!")

def show_users(my_user):
    for user in users:
        if user != my_user:
            print(user)