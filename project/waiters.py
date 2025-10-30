from project.tables import Table


class Waiter:
    def __init__(self, name, age, password, waiter_id):
        self.name = name
        self.age = age
        self.password = password
        self.waiter_id = waiter_id
        self.taken_tables: object = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value.strip() == "":
            raise ValueError("The name cannot be null value!")
        self.__name = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value < 18:
            raise ValueError("The waiter must be at least 18 years old!")
        self.__age = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if len(str(value)) < 4:
            raise ValueError("The password should contain only digits and exactly 4 numbers")
        self.__password = value

    def take_table(self, table: Table):
        # create a table class where you put an is_taken to a table and number
        # check if table is taken
        if table.is_taken:
            print("This table is taken take another table!")
        else:
            self.taken_tables.append(table)
            print(f"Waiter with name: {self.name} took table with number: {table.table_number}")

    def free_table(self, table_number):
        # find the table
        table = next((t for t in self.taken_tables if t.table_number == table_number), None)
        if not table:
            return "Table not found!"
        else:
            self.taken_tables.remove(table)
            table.is_taken = False
            return "Table cleaned successfully!"


