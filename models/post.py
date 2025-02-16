from storage import posts
import storage

class Post:
    def __init__(self, title, content, author):
        self._title = title
        self._content = content
        self._author = author
        self._likes = 0
        self._comments = []
        # Usa o contador global de IDs para posts
        self._id = storage.post_id_counter
        storage.post_id_counter += 1
        self._image = None
        self._video = None

    def getId(self):
        return self._id

    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title

    def getContent(self):
        return self._content

    def setContent(self, content):
        self._content = content

    def getAuthor(self):
        return self._author

    def getLikes(self):
        return self._likes

    def like(self):
        self._likes += 1

    def getComments(self):
        return self._comments

    def addComment(self, comment):
        self._comments.append(comment)

    def setImage(self, image_url):
        self._image = image_url

    def getImage(self):
        return self._image

    def setVideo(self, video_url):
        self._video = video_url

    def getVideo(self):
        return self._video

    def __str__(self):
        return (f"ID:{self.getId()} Autor:{self.getAuthor().getName()}:\n"
                f"    {self.getTitle()}: {self.getContent()}\nLikes: {self.getLikes()}")