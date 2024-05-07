from User import User

class Admin(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, 'admin')
        self.name = name