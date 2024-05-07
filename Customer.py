from User import User

class Customer(User):
    def __init__(self, username, password, name, membership_level, budget):
        super().__init__(username, password, 'customer')
        self.name = name
        self.membership_level = membership_level
        self.budget = budget
