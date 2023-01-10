from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user):

        (id, email, password, name, surname, propic) = user
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.propic = propic