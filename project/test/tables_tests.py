from unittest import TestCase
from project.tables import Table
class TestTables(TestCase):
    def setUp(self):
        self.table = Table(12)
    def test_table_init(self):
        self.assertEqual(12, self.table.table_number)
