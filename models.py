from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self, user):

        (id, username, email, password, name, surname, bio, propic) = user
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.bio = bio
        self.propic = propic