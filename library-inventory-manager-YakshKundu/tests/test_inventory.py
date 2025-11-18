import unittest
from library_manager.book import Book
from library_manager.inventory import LibraryInventory
import os

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.path = "test_catalog.json"
        # ensure a clean file
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass
        self.inv = LibraryInventory(json_path=self.path)

    def tearDown(self):
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass

    def test_add_and_find(self):
        b = Book("Title","Author","ISBN123")
        self.inv.add_book(b)
        found = self.inv.find_by_isbn("ISBN123")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Title")

    def test_issue_and_return(self):
        b = Book("T2","A2","ISBN2")
        self.inv.add_book(b)
        self.assertTrue(self.inv.issue_book("ISBN2"))
        self.assertFalse(self.inv.issue_book("ISBN2"))  # already issued
        self.assertTrue(self.inv.return_book("ISBN2"))
        self.assertFalse(self.inv.return_book("ISBN2"))  # already available

if __name__ == '__main__':
    unittest.main()
