# controllers/post_controller.py
from models.post import Post
from storage import posts

def create_post(user):
    title = input("Qual o título do seu post? ")
    content = input("O que você quer dizer? ")
    post = Post(title, content, user)
    image_question = input("Você quer adicionar uma imagem? (y/n) ")
    if image_question.lower() == 'y':
        image = input("Digite o URL da imagem: ")
        post.setImage(image)
    video_question = input("Você quer adicionar um vídeo? (y/n) ")
    if video_question.lower() == 'y':
        video = input("Digite o URL do vídeo: ")
        post.setVideo(video)
    posts.append(post)
    print(f"Post criado com sucesso: {post.getTitle()}")

def edit_post(user):
    user_posts = [post for post in posts if post.getAuthor() == user]
    if not user_posts:
        print("Você não possui posts para editar.")
        return
    for post in user_posts:
        print(post)
    try:
        post_id = int(input("Digite o ID do post que deseja editar: "))
    except ValueError:
        print("ID inválido.")
        return
    selected_post = next((post for post in user_posts if post.getId() == post_id), None)
    if not selected_post:
        print("Post não encontrado.")
        return
    while True:
        print("\nOpções de edição:")
        print("1) Editar Título")
        print("2) Editar Conteúdo")
        print("3) Voltar")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            new_title = input("Digite o novo título: ")
            selected_post.setTitle(new_title)
            print("Título editado com sucesso!")
        elif choice == '2':
            new_content = input("Digite o novo conteúdo: ")
            selected_post.setContent(new_content)
            print("Conteúdo editado com sucesso!")
        elif choice == '3':
            break
        else:
            print("Opção inválida!")

def delete_post(user):
    user_posts = [post for post in posts if post.getAuthor() == user]
    if not user_posts:
        print("Nenhum post encontrado para deletar.")
        return
    for post in user_posts:
        print(post)
    try:
        post_id = int(input("Digite o ID do post a ser excluído: "))
    except ValueError:
        print("ID inválido.")
        return
    selected_post = next((post for post in user_posts if post.getId() == post_id), None)
    if selected_post:
        posts.remove(selected_post)
        print("Post removido com sucesso!")
    else:
        print("Você não tem permissão para deletar este post ou ele não existe.")

def list_all_posts(user):
    if not posts:
        print("Nenhum post disponível.")
        return
    for post in posts:
        # Se o perfil do autor for privado e o usuário não o segue, ignora o post
        if post.getAuthor()._privacity and post.getAuthor() not in user.getFollowingList():
            continue
        print(post)
        for comment in post.getComments():
            print(f"{comment['user']}: {comment['comment']}")
        print("")
    try:
        like_id = int(input("Digite o ID do post que deseja curtir (ou 0 para voltar): "))
    except ValueError:
        print("ID inválido.")
        return
    if like_id == 0:
        return
    selected_post = next((post for post in posts if post.getId() == like_id), None)
    if selected_post:
        like_post(user, selected_post)
    else:
        print("Post não encontrado.")

def like_post(user, post):
    post.like()
    post.getAuthor().addNotification({
        "user": user,
        "message": f"{user.getName()} curtiu seu post.",
        "is_like": True
    })
    print("Post curtido!")

def comment_post(user, post):
    comment_text = input("Digite seu comentário: ")
    comment = {"user": user.getName(), "comment": comment_text}
    post.addComment(comment)
    post.getAuthor().addNotification({
        "user": user,
        "message": f"{user.getName()} comentou seu post: {comment_text}",
        "is_comment": True,
        "comment": comment_text
    })
    print("Comentário adicionado!")

def search_posts(user):
    search_term = input("Digite o termo de pesquisa: ")
    matching_posts = [post for post in posts if (search_term.lower() in post.getTitle().lower() or search_term.lower() in post.getContent().lower())
                      and (not post.getAuthor()._privacity or post.getAuthor() in user.getFollowingList())]
    if not matching_posts:
        print("Nenhum post encontrado.")
        return
    for post in matching_posts:
        print(post)