from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, name, surname):
        self.id = id
        pass