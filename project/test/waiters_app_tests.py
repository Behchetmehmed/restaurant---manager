import unittest
from unittest.mock import patch
from unittest import TestCase, main

from pyexpat.errors import messages

from project.waiters_app import RestaurantManagement
from project.waiters import Waiter
from project.tables import Table

class TestRestaurantManagementApp(unittest.TestCase):
    def setUp(self):
        self.rm = RestaurantManagement()


    def test_init(self):
        self.assertEqual(self.rm.waiters, [])

        self.assertEqual(self.rm.tables, [])

        self.assertEqual(self.rm.turnover, 0 )

        self.assertEqual(self.rm.total_tables_per_day, 0)


    @patch('builtins.input', side_effect=['Bob', 18, 1234, 4321])
    def test_register_waiter(self, mock_input):
        message = self.rm.register_waiter()

        self.assertEqual(message, "Waiter created and registered successfully!")

        self.assertEqual(len(self.rm.waiters), 1)

        waiter = self.rm.waiters[0]

        self.assertEqual(waiter.name, 'Bob')

        self.assertEqual(waiter.age, 18)

        self.assertEqual(waiter.password, 1234)

        self.assertEqual(waiter.waiter_id, 4321)

    def test_list_all_waiters_without_registered_waiters(self):
        self.assertEqual(self.rm.waiters, [])

        message = self.rm.list_waiters()

        self.assertEqual(message, "No waiters registered!")

    def test_list_all_waiters_with_registered_waiters(self):
        self.assertEqual(self.rm.waiters, [])

        self.rm.waiters.append(Waiter('Bob', 18,1234,4321))

        self.assertEqual(len(self.rm.waiters), 1)

        result = self.rm.list_waiters()

        self.assertEqual(result, f"1. Name: Bob, Waiter ID: 4321")

    @patch('builtins.input', side_effect=[423234])
    def test_unregister_waiter_without_registered_waiters(self, mock_input):
        self.assertEqual(len(self.rm.waiters), 0)

        message = self.rm.unregister_waiter()

        self.assertEqual(message, "No waiter with id: 423234")

    @patch('builtins.input', side_effect=['Bob', 18, 1234, 4321, 4321, 'yes'])
    def test_unregister_waiter_with_registered_waiters(self, mock_input):
        #first we register a waiter
        self.assertEqual(self.rm.waiters, [])

        register = self.rm.register_waiter()

        self.assertEqual(len(self.rm.waiters), 1)

        #now we unregister the waiter
        message = self.rm.unregister_waiter()

        self.assertEqual(message, "Waiter unregistered successfully!")

        self.assertEqual(len(self.rm.waiters), 0)

    @patch('builtins.input', side_effect=['Bob', 18, 1234, 4321, 4321, 'no'])
    def test_unregister_waiter_with_negative_answer_for_confirmation_message(self, mock_input):
        # first we register a waiter
        self.assertEqual(self.rm.waiters, [])

        register = self.rm.register_waiter()

        self.assertEqual(len(self.rm.waiters), 1)

        message = self.rm.unregister_waiter()

        self.assertEqual(message, "Waiter was not unregistered!")

        self.assertEqual(len(self.rm.waiters), 1)

    @patch('builtins.input', side_effect=['Bob', 18, 1234, 4321, 4321, 'invalid'])
    def test_unregister_waiter_with_invalid_confirmation_message(self, mock_input):
        # first we register a waiter
        self.assertEqual(self.rm.waiters, [])

        register = self.rm.register_waiter()

        self.assertEqual(len(self.rm.waiters), 1)

        message = self.rm.unregister_waiter()

        self.assertEqual(message, "Please enter a valid answer!")

        self.assertEqual(len(self.rm.waiters), 1)

    @patch('builtins.input', side_effect=[12])
    def test_create_table(self, mock_input):
        self.assertEqual(self.rm.tables, [])

        message= self.rm.create_table()

        self.assertEqual(message, "New table created successfully!")

        self.assertEqual(len(self.rm.tables), 1)

    @patch('builtins.input', side_effect=[12, 12])
    def test_create_table_with_registered_table(self, mock_input):
        self.assertEqual(self.rm.tables, [])

        register = self.rm.create_table()

        self.assertEqual(len(self.rm.tables), 1)

        message = self.rm.create_table()

        self.assertEqual(message, "Table with this number is already in the restaurant!")


    @patch('builtins.input', side_effect=[12, 4321])
    def test_assign_waiter_to_table_without_an_existing_table(self, mock_input):
        self.assertEqual(self.rm.tables, [])

        message = self.rm.assign_waiter_to_a_table()

        self.assertEqual(message, "Table not found!")

    @patch('builtins.input', side_effect=[12, 12,  4321])
    def test_assign_waiter_to_table_without_an_existing_waiter(self, mock_input):
        #first we register a table
        self.assertEqual(self.rm.tables, [])

        message = self.rm.create_table()


        self.assertEqual(len(self.rm.tables), 1)


        message = self.rm.assign_waiter_to_a_table()

        self.assertEqual(message, "Waiter not found!")

    @patch('builtins.input', side_effect=['Bob', 18, 1234, 4321, 12, 4321])
    def test_assign_waiter_to_a_table_with_table_is_taken(self, mock_input):
        #first we create a table and assign is_taken to True
        table = Table(12)
        table.is_taken = True
        self.rm.tables.append(table)
        self.assertEqual(len(self.rm.tables), 1)

        #second we register a waiter
        self.assertEqual(self.rm.waiters, [])

        register = self.rm.register_waiter()

        self.assertEqual(len(self.rm.waiters), 1)
        message = self.rm.assign_waiter_to_a_table()
        self.assertEqual(message, "Table is already taken!")

    @patch('builtins.input', side_effect=['Bob', 18, 1234, 4321, 12, 4321])
    def test_assign_waiter_to_a_table_valid(self, mock_input):
        # first we create a table and assign is_taken to True
        table = Table(12)
        self.rm.tables.append(table)
        self.assertEqual(len(self.rm.tables), 1)

        # second we register a waiter
        self.assertEqual(self.rm.waiters, [])

        register = self.rm.register_waiter()

        self.assertEqual(len(self.rm.waiters), 1)
        message = self.rm.assign_waiter_to_a_table()
        self.assertEqual(message, f"Table with number: 12 assigned to: Bob")

    def test_list_free_tables_without_any_tables(self):
        self.assertEqual(self.rm.tables, [])

        message = self.rm.list_free_tables()

        self.assertEqual(message, "No tables available!")
    @patch('builtins.input', side_effect=[12])
    def test_list_free_tables_with_active_table(self, mock_input):
        self.assertEqual(self.rm.tables, [])

        register = self.rm.create_table()

        self.assertEqual(len(self.rm.tables), 1)

        message = self.rm.list_free_tables()

        self.assertEqual(message, "Free tables:\nTable: 12")


    def test_list_active_tables_without_any_tables(self):
        self.assertEqual(self.rm.tables, [])

        message = self.rm.list_active_tables()

        self.assertEqual(message, "No tables available!")


    def test_list_active_tables_with_active_table(self):
        #creating a taken table
        table = Table(12)

        table.is_taken = True

        self.rm.tables.append(table)

        self.assertEqual(len(self.rm.tables), 1)

        message = self.rm.list_active_tables()

        self.assertEqual(message, "Active tables:\nTable: 12")

    @patch('builtins.input', side_effect=[213134324])
    def test_get_product_by_code_with_invalid_product_code(self, mock_input):
        message = self.rm.get_product_by_code()

        self.assertEqual(message, "Product not found!")

    @patch('builtins.input', side_effect=[101])
    def test_get_product_by_code_with_valid_code(self, mock_input):
        message = self.rm.get_product_by_code()

        self.assertEqual(message, f"Name: Garlic Bread\n"
                        f"Category: Starter\n"
                        f"Price: 4.5")

    @patch('builtins.input', side_effect=[12, '101'])
    def test_take_order_with_no_table(self, mock_input):
        self.assertEqual(self.rm.tables, [])
        message = self.rm.take_order()

        self.assertEqual(message, "Table not found!")

    @patch('builtins.input', side_effect=[12, '12341'])
    def test_take_order_with_valid_table_but_invalid_product_code(self, mock_input):
        self.assertEqual(self.rm.tables, [])

        table = Table(12)

        self.rm.tables.append(table)

        self.assertEqual(len(self.rm.tables), 1)

        message = self.rm.take_order()

        self.assertEqual(message, "Product is not available!")

    @patch('builtins.input', side_effect=[12, '101'])
    def test_take_order_with_all_valid_inputs(self, mock_input):
        self.assertEqual(self.rm.tables, [])

        table = Table(12)

        self.rm.tables.append(table)

        self.assertEqual(len(self.rm.tables), 1)

        message = self.rm.take_order()

        self.assertEqual(message, "Order taken successfully!")

        self.assertEqual(table.ordered_items, [{'name': 'Garlic Bread', 'category': 'Starter', 'price': 4.5}])

    @patch('builtins.input', side_effect=['12'])
    def test_show_table_orders_with_orders(self, mock_input):
        # Arrange — create a table with orders
        table = Table(table_number=12)
        table.ordered_items = [101, 102]  # table has two orders
        self.rm.tables = [table]

        # Act
        result = self.rm.show_table_orders()

        # Assert — check the formatted string
        expected = (
            "-------Table - 12--------\n"
            "--------------------------\n"
            "1. Garlic Bread - 4.5$.\n"
            "2. French Fries - 3.99$.\n"
            "--------------------\n"
            "Total: 8.49$"
        )
        self.assertEqual(result, expected)

    @patch('builtins.input', side_effect=['99'])
    def test_show_table_orders_table_not_found(self, mock_input):
        # No table 99 exists
        self.rm.tables = []
        result = self.rm.show_table_orders()
        self.assertEqual(result, "Table not found!")

    @patch('builtins.input', side_effect=[12, 101])
    def test_remove_item_from_order_valid(self, mock_input):
        table = Table(12)
        table.ordered_items = [101, 102]
        self.rm.tables = [table]

        message = self.rm.remove_item_from_order()

        self.assertEqual(message, "Product removed successfully!")
        self.assertEqual(table.ordered_items, [102])

    @patch('builtins.input', side_effect=[12, 999])
    def test_remove_item_from_order_product_not_found(self, mock_input):
        table = Table(12)
        table.ordered_items = [101]
        self.rm.tables = [table]

        message = self.rm.remove_item_from_order()
        self.assertEqual(message, "Product not ordered!")

    @patch('builtins.input', side_effect=[99, 101])
    def test_remove_item_from_order_table_not_found(self, mock_input):
        self.rm.tables = []
        message = self.rm.remove_item_from_order()
        self.assertEqual(message, "Table not found!")

    # --------------------------------------------------
    # close_table_bill
    # --------------------------------------------------
    @patch('builtins.input', side_effect=[12])
    def test_close_table_bill_valid(self, mock_input):
        table = Table(12)
        table.ordered_items = [101, 102]
        self.rm.tables = [table]

        message = self.rm.close_table_bill()

        expected = (
            "----------Table - 12--------\n"
            "Ordered items:\n"
            "Garlic Bread - 4.5$\n"
            "French Fries - 3.99$\n"
            "Total: 8.49$"
        )

        self.assertEqual(message, expected)
        self.assertEqual(self.rm.total_tables_per_day, 1)
        self.assertAlmostEqual(self.rm.turnover, 8.49, places=2)

    @patch('builtins.input', side_effect=[99])
    def test_close_table_bill_table_not_found(self, mock_input):
        self.rm.tables = []
        message = self.rm.close_table_bill()
        self.assertEqual(message, "Table not found!")

    def test_daily_summary(self):
        self.rm.total_tables_per_day = 3
        self.rm.turnover = 50.25

        message = self.rm.daily_summary()

        expected = "---------- Papa's Daily Summary - 3--------\n Total: 50.25$"
        self.assertEqual(message, expected)
if __name__ == '__main__':
    main()