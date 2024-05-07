class Transaction:
    def __init__(self, username, product_index, quantity, total_cost, discount,discounted_cost, final_cost, date):
        self.username = username
        self.product_index = product_index
        self.quantity = quantity
        self.total_cost = total_cost
        self.discount = discount
        self.discounted_cost= discounted_cost
        self.final_cost = final_cost
        self.date = tuple(date)