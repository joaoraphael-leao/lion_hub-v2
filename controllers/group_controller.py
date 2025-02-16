# controllers/group_controller.py
from models.group import Group
from storage import groups, users

def create_group(user):
    name = input("Digite o nome do grupo: ")
    description = input("Digite a descrição do grupo: ")
    group = Group(name, description, user)
    groups.append(group)
    print(f"Grupo '{name}' criado com sucesso!")
    return group

def list_groups():
    if not groups:
        print("Nenhum grupo disponível.")
        return
    for i, group in enumerate(groups, start=1):
        print(f"{i}) {group}")

def manage_group(user):
    user_groups = [g for g in groups if g.getFounder() == user or user in g.getMembers()]
    if not user_groups:
        print("Você não participa de nenhum grupo.")
        return
    for i, group in enumerate(user_groups, start=1):
        print(f"{i}) {group.getName()}")
    try:
        choice = int(input("Digite o número do grupo que deseja gerenciar: "))
        selected_group = user_groups[choice - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return
    while True:
        print(f"\nGerenciando o grupo '{selected_group.getName()}':")
        print("1) Ver membros")
        print("2) Adicionar membro")
        print("3) Remover membro")
        print("4) Voltar")
        option = input("Escolha uma opção: ")
        if option == '1':
            members = selected_group.getMembers()
            for i, member in enumerate(members, start=1):
                print(f"{i}) {member.getName()}")
        elif option == '2':
            available_users = [u for u in users if u not in selected_group.getMembers()]
            for u in available_users:
                print(f"{u.getId()} - {u.getName()}")
            try:
                uid = int(input("Digite o ID do usuário que deseja adicionar: "))
            except ValueError:
                print("ID inválido.")
                continue
            user_to_add = next((u for u in available_users if u.getId() == uid), None)
            if user_to_add:
                if selected_group.addMember(user_to_add):
                    print(f"{user_to_add.getName()} adicionado ao grupo.")
                else:
                    print("Erro ao adicionar o membro.")
            else:
                print("Usuário não encontrado.")
        elif option == '3':
            members = selected_group.getMembers()
            for member in members:
                print(f"{member.getId()} - {member.getName()}")
            try:
                uid = int(input("Digite o ID do usuário que deseja remover: "))
            except ValueError:
                print("ID inválido.")
                continue
            user_to_remove = next((m for m in members if m.getId() == uid), None)
            if user_to_remove:
                if user_to_remove == selected_group.getFounder():
                    print("Não é possível remover o fundador do grupo.")
                elif selected_group.removeMember(user_to_remove):
                    print(f"{user_to_remove.getName()} removido do grupo.")
                else:
                    print("Erro ao remover o membro.")
            else:
                print("Usuário não encontrado no grupo.")
        elif option == '4':
            break
        else:
            print("Opção inválida.")