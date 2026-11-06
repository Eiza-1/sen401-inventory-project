"""Unit tests for the Inventory Manager.

Run with:  python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inventory  # noqa: E402
from app import total_stock_value  # noqa: E402
from utils.helpers import highest_stock_item, item_value, lowest_stock_item  # noqa: E402

SAMPLE = [
    {"item_name": "A", "quantity": 2, "price": 100},
    {"item_name": "B", "quantity": 20, "price": 5},
    {"item_name": "C", "quantity": 7, "price": 10},
]


class TestCalculations(unittest.TestCase):
    """Corrective maintenance: value must be quantity x price."""

    def test_item_value(self):
        self.assertEqual(item_value(SAMPLE[0]), 200)

    def test_total_stock_value(self):
        self.assertEqual(total_stock_value(SAMPLE), 200 + 100 + 70)

    def test_total_empty(self):
        self.assertEqual(total_stock_value([]), 0)

    def test_highest_lowest(self):
        self.assertEqual(highest_stock_item(SAMPLE)["item_name"], "B")
        self.assertEqual(lowest_stock_item(SAMPLE)["item_name"], "A")

    def test_highest_lowest_empty(self):
        self.assertIsNone(highest_stock_item([]))
        self.assertIsNone(lowest_stock_item([]))


class TestFeatures(unittest.TestCase):
    """Adaptive maintenance: validation and low-stock check."""

    def test_low_stock(self):
        names = [i["item_name"] for i in inventory.low_stock_items(SAMPLE)]
        self.assertEqual(names, ["A", "C"])

    def test_valid_item(self):
        self.assertEqual(inventory.validate_item(" Router ", 3, 30000),
                         {"item_name": "Router", "quantity": 3, "price": 30000})

    def test_invalid_items(self):
        for bad in [("", 1, 1), ("X", -1, 1), ("X", 1.5, 1), ("X", True, 1), ("X", 1, -5), ("X", 1, "1")]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                inventory.validate_item(*bad)


if __name__ == "__main__":
    unittest.main()
