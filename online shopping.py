import json
import datetime
from User import User
from transaction import Transaction
from product import Product
from Admin import Admin
from Customer import Customer

#By adding tuples, the code ensures that the remarks and date attribute
#are immutable and can be stored and retrieved consistently


class OnlineShop:
    def __init__(self):
        self.users = []
        self.products = []
        self.transactions = []
        self.logged_in_user = None
        self.level_cost = {1: 5, 2: 10, 3: 20}

    def load_data(self):
        try:
            with open("users.json", "r") as file:
                users_data = json.load(file)
                for user_data in users_data:
                    if user_data['role'] == 'customer':
                        customer = Customer(user_data['username'], user_data['password'], user_data['name'],
                                            user_data['membership_level'], user_data['budget'])
                        self.users.append(customer)
                    elif user_data['role'] == 'admin':
                        admin = Admin(user_data['username'], user_data['password'], user_data['name'])
                        self.users.append(admin)
        except FileNotFoundError:
            self.users = []

        try:
            with open("products.json", "r") as file:
                products_data = json.load(file)
                for product_data in products_data:
                    product = Product(product_data['product_index'], product_data['product_name'],
                                      product_data['price'], product_data['manufacturer'], product_data['remarks'])
                    self.products.append(product)
        except FileNotFoundError:
            self.products = []

        try:
            with open("transactions.json", "r") as file:
                transactions_data = json.load(file)
                for transaction_data in transactions_data:
                    transaction = Transaction(transaction_data['username'], transaction_data['product_index'],
                                              transaction_data['quantity'], transaction_data['total_cost'],
                                              transaction_data['discount'], transaction_data['discounted_cost'],
                                              transaction_data['final_cost'],transaction_data['date'])
                    self.transactions.append(transaction)
        except FileNotFoundError:
            self.transactions = []

    def save_data(self):
        users_data = []
        for user in self.users:
            user_data = {
                'username': user.username,
                'password': user.password,
                'role': user.role,
                'name': user.name
            }
            if isinstance(user, Customer):
                user_data['membership_level'] = user.membership_level
                user_data['budget'] = user.budget
            users_data.append(user_data)

        with open("users.json", "w") as file:
            json.dump(users_data, file, indent=4)

        products_data = []
        for product in self.products:
            product_data = {
                'product_index': product.product_index,
                'product_name': product.product_name,
                'price': product.price,
                'manufacturer': product.manufacturer,
                'remarks': tuple(product.remarks)
            }
            products_data.append(product_data)

        with open("products.json", "w") as file:
            json.dump(products_data, file, indent=4)

        transactions_data = []
        for transaction in self.transactions:
            transaction_data = {
                'username': transaction.username,
                'product_index': transaction.product_index,
                'quantity': transaction.quantity,
                'total_cost': transaction.total_cost,
                'discount': transaction.discount,
                'discounted_cost':transaction.discounted_cost,
                'final_cost': transaction.final_cost,
                'date': tuple(transaction.date) #convert date into tuple
            }
            transactions_data.append(transaction_data)

        with open("transactions.json", "w") as file:
            json.dump(transactions_data, file, indent=4)

    def register(self):
        username = input("Enter username: ")
        if self.is_username_taken(username):
            print("Username already exists.")
            return

        password = input("Enter password (at least 6 characters): ")
        if len(password) < 6:
            print("Password must be at least 6 characters.")
            return

        role = input("Enter role (admin/customer): ")
        if role.lower() not in ['admin', 'customer']:
            print("Invalid role.")
            return

        if role.lower() == 'admin':
            name = input("Enter name: ")
            admin = Admin(username, password,name)
            self.users.append(admin)
        elif role.lower() == 'customer':
            name = input("Enter name: ")
            budget = float(input("Enter budget: "))
            customer = Customer(username, password, name, 0, budget)
            self.users.append(customer)

        self.save_data()
        print("Registration successful.")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        for user in self.users:
            if user.username == username and user.password == password:
                self.logged_in_user = user
                print(f"Logged in as {user.username} ({user.role}).")
                return

        print("Invalid username or password.")

    def logout(self):
        self.logged_in_user = None
        print("Logged out.")

    def is_username_taken(self, username):
        for user in self.users:
            if user.username == username:
                return True
        return False

    def add_product(self):
        if not isinstance(self.logged_in_user, Admin):
            print("You must be an admin to perform this action.")
            return

        product_index =int(input("Enter product index(in integer): "))
        for product in self.products:
            if product.product_index == product_index:
                print("product index must be unique and cannot be repeated")
                return

        product_name = input("Enter product name: ")
        price = float(input("Enter price: "))
        manufacturer = input("Enter manufacturer: ")
        remarks = str(input("Enter remarks: "))
        x = remarks.split()
        y= tuple(x)

        product = Product(product_index, product_name, price, manufacturer, y)
        self.products.append(product)
        self.save_data()
        print("Product added successfully.")

    def remove_product(self, *args):
        if not isinstance(self.logged_in_user, Admin):
            print("You must be an admin to perform this action.")
            return

        if not args:
            print("No product indices provided.")
            return

        removed_count = 0
        for product_index in args:
            product_index = int(product_index)
            for product in self.products:
                if product.product_index == product_index:
                    self.products.remove(product)
                    removed_count += 1

        if removed_count > 0:
            self.save_data()
            print(f"{removed_count} product(s) removed successfully.")
        else:
            print("No matching products found.")

    def update_product(self):
        if not isinstance(self.logged_in_user, Admin):
            print("You must be an admin to perform this action.")
            return

        product_index = int(input("Enter product index to update: "))
        for product in self.products:
            if product.product_index == product_index:
                product.product_name = input("Enter new product name: ")
                product.price = float(input("Enter new price: "))
                product.manufacturer = input("Enter new manufacturer: ")
                R = str(input("Enter new remarks: "))
                r= R.split()
                product.remarks = tuple(r)
                self.save_data()
                print("Product updated successfully.")
                return

        print("Product not found.")

    def read_products(self):
        print("Product Listing:")
        for product in self.products:
            x=" ".join(product.remarks)
            print(f"Index: {product.product_index}, Name: {product.product_name}, "
                  f"Price: ${product.price}, Manufacturer: {product.manufacturer}, "
                  f"Remarks: {x}\n")


    def read_transaction(self):
        if not isinstance(self.logged_in_user, Admin):
            print("You must be an admin to perform this action.")
            return
        print("transaction history:")
        for transaction in self.transactions:
            y = " ".join(transaction.date)
            print(f"Customer username: {transaction.username},Product index: {transaction.product_index},"
                  f"quantity:{transaction.quantity},total cost:{transaction.total_cost},"
                  f"discount:{transaction.discount},discounted cost:{transaction.discounted_cost},"
                  f"final cost: {transaction.final_cost},date: {y}\n")

    def read_customer(self):
        if not isinstance(self.logged_in_user, Admin):
            print("You must be an admin to perform this action.")
            return

        print("User Listing:")
        for user in self.users:
            if isinstance(user, Customer):
                print(f"Username: {user.username}, Role: {user.role},Name: {user.name},Membership Level: {user.membership_level}, Budget: {user.budget}")

    def make_transaction(self):
        if not isinstance(self.logged_in_user, Customer):
            print("You must be a customer to perform this action.")
            return

        self.read_products()
        print("Budget:",self.logged_in_user.budget)
        product_index = int(input("Enter product index to purchase: "))
        product = self.find_product_by_index(product_index)
        if product is None:
            print("Product not found.")
            return

        quantity = int(input("Enter quantity to purchase: "))
        if quantity <= 0:
            print("Invalid quantity.")
            return

        total_cost = product.price * quantity
        discount = self.calculate_discount(self.logged_in_user.membership_level)
        discounted_cost = total_cost *discount
        final_cost = total_cost - discounted_cost

        if final_cost > self.logged_in_user.budget:
            print("Insufficient budget.")
            return

        date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


        self.logged_in_user.budget -= final_cost
        transaction = Transaction(self.logged_in_user.username, product_index, quantity, total_cost, discount,discounted_cost,
                                  final_cost, date.split())
        self.transactions.append(transaction)
        self.save_data()
        print("Transaction successful.")
        print("Product brought: index:",product_index)
        print("Quantity:",quantity)
        print("Total cost:",total_cost)
        print("Discount%:",100*discount)
        print("Discounted cost:", discounted_cost)
        print("Final price: ",final_cost)
        print("Remaining budget:",self.logged_in_user.budget)


    def add_money(self):
        if not isinstance(self.logged_in_user, Customer):
            print("You must be a customer to perform this action.")
            return

        amount = float(input("Enter the amount to add: "))

        if amount <= 0:
            print("Invalid amount.")
            return

        self.logged_in_user.budget += amount
        print("remaining budget:",self.logged_in_user.budget)
        self.save_data()
        print("Money added successfully.")

    def calculate_discount(self, membership_level):
        if membership_level == 0:
            return 0
        elif membership_level == 1:
            return 0.05
        elif membership_level == 2:
            return 0.1
        elif membership_level == 3:
            return 0.15

    def membership_cost_change(self):
        if not isinstance(self.logged_in_user, Admin):
            print("You must be a admin to perform this action.")
            return
        print("Membership level increase at 1 level at a time")
        print("increase membership level from 0 to 1 cost",self.level_cost.get(1)," dollars")
        print("increase membership level from 1 to 2 cost",self.level_cost.get(2)," dollars")
        print("increase membership level from 2 to 3 cost",self.level_cost.get(3)," dollars")
        print("Please input which membership level cost you would change:\n","1. level 0 to 1\n","2. level 1 to 2\n","3. level 2 to 3\n")
        x = int(input("Please enter the amount of cost you wish to change: "))
        if(x == 1 or x==2 or x==3):
            n_cost= int(input("Please enter the amount of payment: "))
        else:
            print("invalid input")
            return
        self.level_cost[x] = n_cost
        print("membership level from",x-1,"to",x,"cost",self.level_cost.get(1)," dollars")



    def increase_membership_level(self):
        if not isinstance(self.logged_in_user, Customer):
            print("You must be a customer to perform this action.")
            return

        if self.logged_in_user.membership_level == 3:
            print("You have reached the maximum membership level.")
            return

        next_level = self.logged_in_user.membership_level + 1
        cost = self.level_cost.get(next_level, 0)

        if cost == 0:
            print("Invalid membership level.")
            return

        if cost > self.logged_in_user.budget:
            print("Insufficient budget.")
            return

        if self.logged_in_user.membership_level == 0:
            print("membership level 1 cost",self.level_cost.get(1)," dollars and will have 5% discount upon any transaction")
        elif self.logged_in_user.membership_level == 1:
            print("membership level 2 cost ",self.level_cost.get(2)," dollars and will have 10% discount upon any transaction")
        elif self.logged_in_user.membership_level == 2:
            print("membership level 3 cost ",self.level_cost.get(3)," dollars and will have 15% discount upon any transaction")
        else:
            return
        x = str(input("do you want to increase your membership level?(y/n)"))
        if(x=="Y" or x=="y"):
            self.logged_in_user.budget -= cost
            self.logged_in_user.membership_level = next_level
            self.save_data()
            print(f"Membership level increased to {next_level}.")
            print("remaining budget:",self.logged_in_user.budget)
        elif (x=="n" or x == "N"):
            print("membership level was not increase")
            return
        else:
            print("invalid input")

    def find_product_by_index(self, product_index):
        for product in self.products:
            if product.product_index == product_index:
                return product
        return None

    def show_menu(self,**menu):
        for x,y in menu.items():
            print("{}. {}\n".format(y,x))

    def run(self):
        self.load_data()

        while True:
            print("\n-------- Online Shopping --------")
            self.show_menu(Register=1,Login=2,Exit=3)
            choice = input("Enter your choice: ")

            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
                if self.logged_in_user is not None:
                    if self.logged_in_user.role == 'admin':
                        while True:
                            print("\n-------- Admin Menu --------")
                            print("1. Read all customer data")
                            print("2. Add product")
                            print("3. Remove product")
                            print("4. Update product")
                            print("5. Read product listing")
                            print("6. Read transaction history")
                            print("7. Change cost of membership")
                            print("8. Logout")

                            admin_choice = input("Enter your choice: ")

                            if admin_choice == "1":
                                self.read_customer()
                            elif admin_choice == "2":
                                self.add_product()
                            elif admin_choice == "3":
                                self.read_products()
                                product_indexes = input("Please enter product indexes you want to delete (separated by spaces): ")
                                self.remove_product(*product_indexes.split())
                            elif admin_choice == "4":
                                self.read_products()
                                self.update_product()
                            elif admin_choice == "5":
                                self.read_products()
                            elif admin_choice == "6":
                                self.read_transaction()
                            elif admin_choice == "7":
                                self.membership_cost_change()
                            elif admin_choice == "8":
                                self.logout()
                                break
                            else:
                                print("Invalid choice.")
                    elif self.logged_in_user.role == 'customer':
                        while True:
                            print("\n-------- Customer Menu --------")
                            print("Membership level:",self.logged_in_user.membership_level)
                            print("remaining budget:",self.logged_in_user.budget)
                            print("1. Increase membership level")
                            print("2. Make transaction")
                            print("3. Read product listing")
                            print("4. Add money to budget")
                            print("5. Logout")

                            customer_choice = input("Enter your choice: ")

                            if customer_choice == "1":
                                self.increase_membership_level()
                            elif customer_choice == "2":
                                self.make_transaction()
                            elif customer_choice == "3":
                                self.read_products()
                            elif customer_choice == "4":
                                self.add_money()
                            elif customer_choice == "5":
                                self.logout()
                                break
                            else:
                                print("Invalid choice.")
            elif choice == "3":
                self.save_data()
                print("Thank you for using our Online Shopping system.")
                break
            else:
                print("Invalid choice.")


shop = OnlineShop()
shop.run()
