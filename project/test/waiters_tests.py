import unittest
from unittest import main

from project.waiters import Waiter

class TestWaiter(unittest.TestCase):

    def setUp(self):
        self.waiter = Waiter('Berk', 18, 1111, 2222)

    def test_init(self):
        self.assertEqual(self.waiter.name, 'Berk')
        self.assertEqual(self.waiter.age, 18)
        self.assertEqual(self.waiter.password, 1111)
        self.assertEqual(self.waiter.waiter_id, 2222)

    def test_property_name_invalid(self):
        self.assertEqual(self.waiter.name, 'Berk')
        with self.assertRaises(ValueError) as err:
            self.waiter.name = "    "

        self.assertEqual(str(err.exception), "The name cannot be null value!")

    def test_property_age_invalid(self):
        self.assertEqual(self.waiter.age, 18)
        with self.assertRaises(ValueError) as err:
            self.waiter.age = 11

        self.assertEqual(str(err.exception), "The waiter must be at least 18 years old!")



    def test_password_setter_invalid(self):
        with self.assertRaises(ValueError) as err:
            self.waiter.password = 123
        self.assertEqual(str(err.exception), "The password should contain only digits and exactly 4 numbers")
        #trying with shorter value
        with self.assertRaises(ValueError) as err:
            self.waiter.password = 12
        self.assertEqual(str(err.exception), "The password should contain only digits and exactly 4 numbers")


if __name__ == "__main__":
    main()
