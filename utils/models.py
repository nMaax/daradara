from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user):

        (id, email, password, name, surname, propic, priv_owner, priv_follows, priv_saves) = user
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.propic = propic
        self.privacy = [priv_owner, priv_follows, priv_saves]