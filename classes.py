from main import postsList, usersList, POSTS_ID_VARIABLE, USERS_ID_VARIABLE





class Post:
    def __init__(self, title, content, author, USERS_ID_VARIABLE):
        self._title = title
        self._content = content
        self._author = author
        self._id = USERS_ID_VARIABLE
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
    def getId(self):
        return self._id
    def setTitle(self, title):
        self._title = title
    def setContent(self, content):
        self._content = content
    def setImage(self, image_url):
        self._image = image_url
    def setVideo(self, video_url):
        self._video = video_url

    def __str__(self):
        return f"ID:{self.getId()} Autor:{self.getAuthor().getName()}:\n    {self.getTitle}: {self.getContent}\n"

class User:
    def __init__(self, name, email, password, privacity, id):
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
        return my_posts

    def createPost(self, post_id_variable):
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
        print(f"Post criado com sucesso: {post.getTitle()}")

    def editPost(self):
        auxiliarPosts = self.seeMyPosts()
        for post in auxiliarPosts:
            print(post)

        post_id = input("Select the id for the post that you want to change")

        for post in auxiliarPosts:
            if post_id == auxiliarPosts.getId():
                change_title = input("type 1 to edit the title")
                if change_title == 1:
                    new_title = input("type the new title of the post")
                    post.setTitle(new_title)
                change_description = input("type 1 to edit the description")
                if change_description == 1:
                    new_description = input("type the new description of the post")
                    post.setContent(new_description)
                change_img = input("type 1 to edit the image")
                if change_img == 1:
                    new_img = input("type the url of the new image")
                    post.setImage(new_img)
                change_video = input("type 1 to edit the video")
                if change_video == 1:
                    new_video = input("type the url of the new video")
                    post.setImage(new_video)
                print("Post updated!")
                return

        print("No post with this ID found in your posts")

    def deletePost(self):
        my_posts = self.seeMyPosts()
        for post in my_posts:
            print(post)
        id = input("Type the id of the post that you want to delete")
        for post in my_posts:
            if post.getId() == id:
                postsList.remove(post)
                return
        print("Você não tem permissão para excluir esse post")

    def _deleteAccount(self):
        usersList.remove(self)

    def __str__(self):
        print(f"""User: {self.getName()}; e-mail: {self.getEmail()}""")