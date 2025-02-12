usersList = []
postsList = []
user_id_variable = 1
post_id_variable = 1

class Post:
    def __init__(self, title, content, author, posts_id_variable):
        self._title = title
        self._content = content
        self._author = author
        self._id = posts_id_variable
        self._image = None
        self._video = None

    def getId(self):
        return self._id
    def getAuthor(self):
        return self._author

    def getTitle(self):
        return self._title
    def getContent(self):
        return self._content
    def setTitle(self, title):
        self._title = title
    def setContent(self, content):
        self._content = content
    def setImage(self, image_url):
        self._image = image_url
    def setVideo(self, video_url):
        self._video = video_url

    def __str__(self):
        return f"ID:{self.getId()} Autor:{self.getAuthor().getName()}:\n    {self.getTitle()}: {self.getContent()}\n"

class User:
    def __init__(self, name, email, password, id):
        self._name = name
        self._email = email
        self._password = password
        self._id = id
        self._followingList = []
        self._followersList = []

    def getId(self):
        return self._id
    def getName(self):
        return self._name
    def getEmail(self):
        return self._email
    def setName(self, newName):
        self._name = newName
    def setEmail(self, newEmail):
        self._email = newEmail

    def set_password(self, newPassword):
        self._password = newPassword

    def getFollowingList(self):
        return self._followingList

    def getFollowersList(self):
        print(f"People who follows {self.getName()}")
        for person in self._followersList:
            print(person.getName())
    def seeMyPosts(self):
        my_posts = [post for post in postsList if post.getAuthor() == self]
        if not my_posts:
            print("Nenhum post encontrado.")
            return
        for post in my_posts:
            print(post)
        return my_posts

    def createPost(self):
        global post_id_variable
        title = input("Qual o título do seu post? ")
        content = input("O que você quer dizer? ")
        post = Post(title, content, self, post_id_variable)
        image_question = input("Você quer adicionar uma imagem? (y/n) ")
        if image_question.lower() == 'y':
            image = input("Digite o URL da imagem: ")
            post.setImage(image)

        video_question = input("Você quer adicionar um video ? (y/n) ")
        if video_question.lower() == 'y':
            video = input("Digite o URL do vídeo: ")
            post.setVideo(video)

        postsList.append(post)
        post_id_variable += 1
        print(f"Post criado com sucesso: {post.getTitle()}")

    def editPost(self):
        auxiliarPosts = self.seeMyPosts()
        for post in auxiliarPosts:
            print(post)

        post_id = int(input("Select the id for the post that you want to change"))

        for post in auxiliarPosts:
            if post_id == post.getId():
                change_title = input("type 1 to edit the title")
                if change_title == "1":
                    new_title = input("type the new title of the post")
                    post.setTitle(new_title)
                change_description = input("type 1 to edit the description")
                if change_description == "1":
                    new_description = input("type the new description of the post")
                    post.setContent(new_description)
                change_img = input("type 1 to edit the image")
                if change_img == "1":
                    new_img = input("type the url of the new image")
                    post.setImage(new_img)
                change_video = input("type 1 to edit the video")
                if change_video == "1":
                    new_video = input("type the url of the new video")
                    post.setVideo(new_video)
                print("Post updated!")
                return

        print("No post with this ID found in your posts")

    def deletePost(self):
        global post_id_variable
        my_posts = self.seeMyPosts()
        for post in my_posts:
            print(post)
        id = int(input("Type the id of the post that you want to delete"))
        for post in my_posts:
            if post.getId() == id:
                postsList.remove(post)
                print("deletado com sucesso")
                return
        print("Você não tem permissão para excluir esse post")

    def _deleteAccount(self):
        for post in postsList:
            if post.getAuthor() == self:
                postsList.remove(post)
        usersList.remove(self)

    def __str__(self):
        return f"""User: {self.getName()}; e-mail: {self.getEmail()}"""


def createPassword():
    while True:
        password = input("Digite sua senha: ")
        confirmPassword = input("Confirme sua senha: ")
        if password == confirmPassword:
            return password
        print("Senhas não conferem! Tente novamente.")

def follow_someone(myUser):
    print("Escolha alguém para seguir")
    for user in usersList:
        if user == myUser:
            continue
        print(user)
    followed_profile_name = input("Digite o nome do usuário a seguir: ")
    for user in usersList:
        if followed_profile_name == user.getName():
            myUser._followingList.append(user)
            user._followersList.append(myUser)
            print(f"Você começou a seguir {user.getName()}")
            return
    print("Não encontramos esse usuário! Verifique se o nome foi digitado corretamente.")

def add_new_user():
    global user_id_variable
    print("hello")
    email = input("Diga seu email: ")
    username = input("Diga seu nome: ")
    for user in usersList:
        if user.getName() == username or user.getEmail() == email:
            print("Email ou senha já tem uma conta criada")
            user_id_variable -= 1
            return
    else:
        password = createPassword()
        user = User(username, email, password, id=user_id_variable)
        usersList.append(user)
        print(f"Usuário {username} criado com sucesso!")
        return user

def menu_de_conta(user):
    global post_id_variable
    global user_id_variable
    opcao = input("""
    O que deseja ?
    1) Sair
    2) Criar post
    3) Editar post
    4) Deletar post
    5) deletar conta
    6) seguir alguem
    7) mudar nome
    8) mudar email
    9) mudar senha""")

    if opcao == "1":
        return
    if opcao == "2":
        user.createPost()
        post_id_variable += 1
        return
    if opcao == "3":
        user.editPost()
        return
    if opcao == "4":
        user.deletePost()
        return
    if opcao == "5":
        user._deleteAccount()
        user_id_variable -= 1
        return
    if opcao == "6":
        follow_someone(user)
        return
    if opcao == "7":
        nome = input("digite o novo nome")
        for auxiliarUser in usersList:
            if auxiliarUser.getName() == nome:
                print("nome ja esta sendo usado")
                return
        user.setName(nome)
    if opcao == "8":
        email = input("digite o novo email")
        for auxiliarUser in usersList:
            if (auxiliarUser.getEmail() == email):
                print("nome ja esta sendo usado")
                return
        user.setEmail(email)
    if opcao == "9":
        senha = input("Digite a nova senha")
        user._password = senha
def see_users():
    for user in usersList:
        print(user)
def seePosts():
    for post in postsList:
        print(post)

def menu():
    global user_id_variable
    global post_id_variable
    while(1):
        opcao = input("""Options:
        1) sair
        2) criar uma conta
        3) menu de conta
        4) Ver usuários
        5) Ver todos os posts
        """)
        if opcao == "1":
            return
        elif opcao == "2":
            add_new_user()
            user_id_variable += 1
        elif opcao == "3":
            name = input("Digite seu nome")
            password = input("Digite sua senha")
            myUser = None
            for user in usersList:
                if user.getName() == name and user._password == password:
                    myUser = user
                    break

            if myUser:
                menu_de_conta(user=myUser)
            else:
                print("login ou senha incorretos")

        elif opcao == "4":
            see_users()
        elif opcao == "5":
            seePosts()

menu()