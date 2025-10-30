from project.waiters import Waiter
from project.tables import Table
from project.products import products


class RestaurantManagement:

    def __init__(self):
        self.waiters = []
        self.tables = []
        self.turnover = 0
        self.total_tables_per_day = 0

    def register_waiter(self):
        name = input("Enter waiters name: ")
        age = int(input("Enter waiters age: "))
        password = int(
            input("Enter a password for logging in the system. The password must contain a 4-digit number: "))
        waiter_id = int(input("Enter a 4-digit waiter id: "))
        waiter = Waiter(name, age, password, waiter_id)
        self.waiters.append(waiter)
        return "Waiter created and registered successfully!"

    def list_waiters(self):
        counter = 1
        result = []
        for waiter in self.waiters:
            result.append(f"{counter}. Name: {waiter.name}, Waiter ID: {waiter.waiter_id}")
            counter += 1
        if not result:
            return "No waiters registered!"

        return '\n'.join(result)

    def unregister_waiter(self):
        waiters_id = int(input("Please enter waiters id: "))
        # check if waiter exists
        waiter = next((w for w in self.waiters if w.waiter_id == waiters_id), None)
        if waiter is None:
            return f"No waiter with id: {waiters_id}"
        # confirmation for unregistering
        answer = input("Please confirm your choice of unregistering the waiter yes/no").lower()
        if answer == "no":
            return "Waiter was not unregistered!"
        elif answer == "yes":
            self.waiters.remove(waiter)
            return "Waiter unregistered successfully!"
        else:
            return "Please enter a valid answer!"


    def create_table(self):
        table_number = int(input("Please enter the tables number: "))
        # check if table is already in the list
        for table in self.tables:
            if table.table_number == table_number:
                return "Table with this number is already in the restaurant!"

        new_table = Table(table_number)
        self.tables.append(new_table)
        return "New table created successfully!"


    def assign_waiter_to_a_table(self):
        # find table and waiter
        table_number = int(input("Please enter the tables number: "))
        waiter_id = int(input("Please enter a waiter id: "))
        table = next((t for t in self.tables if table_number == t.table_number), None)
        waiter = next((w for w in self.waiters if w.waiter_id == waiter_id), None)
        if table is None:
            return "Table not found!"
        elif waiter is None:
            return "Waiter not found!"
        # check if table available
        if table.is_taken:
            return "Table is already taken!"

        table.waiter_assigned = waiter
        table.is_taken = True
        return f"Table with number: {table_number} assigned to: {waiter.name}"


    def list_free_tables(self):
        if not self.tables:
            return "No tables available!"
        active_tables = [t for t in self.tables if not t.is_taken]
        result = ["Free tables:"]

        for table in active_tables:
            result.append(f"Table: {table.table_number}")
        return '\n'.join(result)

    def list_active_tables(self):
        if not self.tables:
            return "No tables available!"
        active_tables = [t for t in self.tables if t.is_taken]
        result = ["Active tables:"]
        for table in active_tables:
            result.append(f"Table: {table.table_number}")
        return '\n'.join(result)

    def show_menu(self):
        counter = 1
        for key in products:
            print(f"{counter}. {products[key]['name']}")
            counter += 1

    def get_product_by_code(self):
        code = int(input("Enter product code: "))
        for key in products.keys():
            if code == key:
                return (f"Name: {products[key]['name']}\n"
                        f"Category: {products[key]['category']}\n"
                        f"Price: {str(products[key]['price'])}")
        return 'Product not found!'

        # --- Orders & Billing ---

    def take_order(self):
        #check if table exist
        table_number = int(input('Enter table number: '))
        product_codes = input("Enter product codes (separated by spaces): ").split()
        int_product_codes = [int(c) for c in product_codes]
        table = next((t for t in self.tables if table_number == t.table_number), None)
        if table is None:
            return "Table not found!"
        for product in int_product_codes:
            if product not in products.keys():
                return  "Product is not available!"
            table.ordered_items.append(products[product])
        return "Order taken successfully!"

    def show_table_orders(self):
        table_number = int(input('Enter table number: '))
        table = next((t for t in self.tables if table_number == t.table_number), None)
        if table is None:
            return "Table not found!"
        result = [f"-------Table - {table.table_number}--------", "--------------------------"]
        counter = 1
        total = 0
        for product in table.ordered_items:
            result.append(f"{counter}. {products[product]['name']} - {products[product]['price']}$.")
            counter += 1
            total += products[product]['price']

        result.append("--------------------")
        result.append(f"Total: {total:.2f}$")
        return '\n'.join(result)

    def remove_item_from_order(self):
        table_number = int(input("Enter table number: "))
        product_code = int(input("Enter product code: "))
        table = next((t for t in self.tables if table_number == t.table_number), None)

        if table is None:
            return "Table not found!"

        if product_code in table.ordered_items:
            table.ordered_items.remove(product_code)
            return "Product removed successfully!"
        else:
            return "Product not ordered!"



    def close_table_bill(self):
        table_number = int(input("Enter table number: "))
        table = next((t for t in self.tables if t.table_number == table_number), None)
        if table is None:
            return "Table not found!"
        total_bill = 0
        result = [f"----------Table - {table_number}--------", "Ordered items:"]
        for product in table.ordered_items:
            total_bill += products[product]['price']
            result.append(f"{products[product]['name']} - {products[product]['price']}$")

        result.append(f"Total: {total_bill:.2f}$")
        self.total_tables_per_day += 1
        self.turnover += total_bill
        return '\n'.join(result)

    def daily_summary(self):
        result = [f"---------- Papa's Daily Summary - {self.total_tables_per_day}--------\n Total: {self.turnover:.2f}$"]
        return '\n'.join(result)
