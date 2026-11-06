"""Tests for the SQLite layer and the JSON -> SQLite migration.

Each test uses its own temporary database file.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventory_app import config, controllers, database, migrate  # noqa: E402
from inventory_app.models import ItemCreate, ItemUpdate  # noqa: E402


class TempDBTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._old_db = config.DB_PATH
        config.DB_PATH = Path(self.tmp.name) / "test.db"
        database.init_db()

    def tearDown(self):
        config.DB_PATH = self._old_db
        self.tmp.cleanup()


class TestDatabase(TempDBTestCase):
    def test_crud(self):
        item = database.create_item(ItemCreate(item_name="Router", quantity=3, price=30000))
        self.assertEqual(item.id, 1)
        self.assertEqual(database.get_item(1).item_name, "Router")

        updated = database.update_item(1, ItemUpdate(quantity=9))
        self.assertEqual((updated.quantity, updated.price), (9, 30000))

        self.assertTrue(database.delete_item(1))
        self.assertIsNone(database.get_item(1))
        self.assertFalse(database.delete_item(1))

    def test_duplicate_name_rejected(self):
        database.create_item(ItemCreate(item_name="Router", quantity=3, price=1))
        with self.assertRaises(database.DuplicateItemError):
            database.create_item(ItemCreate(item_name="Router", quantity=1, price=1))

    def test_controller_not_found(self):
        with self.assertRaises(controllers.ItemNotFoundError):
            controllers.get_item(99)


class TestMigration(TempDBTestCase):
    def test_migrate_is_idempotent_and_rejects_bad_rows(self):
        src = Path(self.tmp.name) / "legacy.json"
        src.write_text(json.dumps([
            {"item_name": "Laptop", "quantity": 10, "price": 450000},
            {"item_name": "Mouse", "quantity": 50, "price": 5000},
            {"item_name": "Broken", "quantity": -1, "price": 5},
        ]))
        self.assertEqual(migrate.migrate(src), (2, 0, 1))
        self.assertEqual(migrate.migrate(src), (0, 2, 1))
        self.assertEqual(controllers.stock_summary().total_value, 4_750_000)


if __name__ == "__main__":
    unittest.main()
