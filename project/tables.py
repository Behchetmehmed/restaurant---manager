class Table:
    def __init__(self, table_number):
        self.table_number = table_number
        self.is_taken = False
        self.ordered_items = []
        self.waiter_assigned: object = object