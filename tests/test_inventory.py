"""Unit tests for models, utils and controllers (no storage needed).

Run with:  python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import ValidationError  # noqa: E402

from inventory_app import controllers  # noqa: E402
from inventory_app.models import Item, ItemCreate  # noqa: E402
from inventory_app.utils import format_money, item_value, total_value  # noqa: E402

SAMPLE = [
    Item(id=1, item_name="A", quantity=2, price=100),
    Item(id=2, item_name="B", quantity=20, price=5),
    Item(id=3, item_name="C", quantity=7, price=10),
]


class TestUtils(unittest.TestCase):
    def test_item_value(self):
        self.assertEqual(item_value(SAMPLE[0]), 200)

    def test_total_value(self):
        self.assertEqual(total_value(SAMPLE), 370)
        self.assertEqual(total_value([]), 0)

    def test_format_money(self):
        self.assertEqual(format_money(6835000, "NGN"), "NGN 6,835,000.00")


class TestSummary(unittest.TestCase):
    def test_summary(self):
        s = controllers.stock_summary(SAMPLE, threshold=10)
        self.assertEqual((s.total_items, s.total_units, s.total_value), (3, 29, 370))
        self.assertEqual(s.highest_stock.item_name, "B")
        self.assertEqual(s.lowest_stock.item_name, "A")
        self.assertEqual([i.item_name for i in s.low_stock], ["A", "C"])

    def test_summary_empty(self):
        s = controllers.stock_summary([])
        self.assertEqual(s.total_value, 0)
        self.assertIsNone(s.highest_stock)
        self.assertIsNone(s.lowest_stock)


class TestValidation(unittest.TestCase):
    def test_valid_item_is_stripped(self):
        self.assertEqual(ItemCreate(item_name=" Router ", quantity=3, price=30000).item_name, "Router")

    def test_invalid_items(self):
        for bad in [("", 1, 1), ("X", -1, 1), ("X", 1.5, 1), ("X", True, 1), ("X", 1, -5), ("X", 1, "1")]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                ItemCreate(item_name=bad[0], quantity=bad[1], price=bad[2])


if __name__ == "__main__":
    unittest.main()
