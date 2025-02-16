from storage import users
import storage

class User:
    def __init__(self, name, email, password, privacity):
        self._name = name
        self._email = email
        self._password = password
        # Usa o contador global de IDs
        self._id = storage.user_id_counter
        storage.user_id_counter += 1
        self._notifications = []
        self._followingList = []
        self._followersList = []
        self._privacity = privacity
        self._active = True

    def __str__(self):
        return f"{self._name} - {self._email}"

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email

    def getPassword(self):
        return self._password

    def setPassword(self, password):
        self._password = password

    def getId(self):
        return self._id

    def isActive(self):
        return self._active

    def addNotification(self, notification):
        self._notifications.append(notification)

    def getNotifications(self):
        return self._notifications

    def follow(self, other_user):
        if other_user not in self._followingList:
            self._followingList.append(other_user)
            other_user._followersList.append(self)

    def getFollowingList(self):
        return self._followingList

    def getFollowersList(self):
        return self._followersList

    def deleteAccount(self):
        self._active = False
        self._name = ""
        self._email = ""
        self._password = ""
        self._notifications = []
        self._followingList = []
        self._followersList = []