"""Inventory data module for the Inventory Manager.

Holds the in-memory list of stock items and the functions that validate,
add and filter them.
"""

from typing import TypedDict

# --- Configuration constants -----------------------------------------------
LOW_STOCK_THRESHOLD = 10
CURRENCY = "NGN"


class Item(TypedDict):
    """A single stock item."""

    item_name: str
    quantity: int
    price: float


# Python 3.12+ type alias statement (PEP 695)
type Inventory = list[Item]

# --- Data -------------------------------------------------------------------
inventory: Inventory = [
    {"item_name": "Laptop", "quantity": 10, "price": 450000},
    {"item_name": "Mouse", "quantity": 50, "price": 5000},
    {"item_name": "Keyboard", "quantity": 30, "price": 12000},
    {"item_name": "Monitor", "quantity": 8, "price": 150000},
    {"item_name": "USB Cable", "quantity": 100, "price": 1500},
]


def validate_item(item_name: str, quantity: int, price: float) -> Item:
    """Check the fields of a new item and return a clean Item record.

    Raises:
        ValueError: If the name is empty, or quantity/price is negative or
            of the wrong type (bool is rejected because it is a subclass of int).
    """
    if not isinstance(item_name, str) or not item_name.strip():
        raise ValueError("Item name must be a non-empty string")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
        raise ValueError("Quantity must be a whole number of 0 or more")
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        raise ValueError("Price must be a number of 0 or more")
    return {"item_name": item_name.strip(), "quantity": quantity, "price": price}


def add_item(item_name: str, quantity: int, price: float) -> Item:
    """Validate and append a new item, returning the stored record."""
    record = validate_item(item_name, quantity, price)
    inventory.append(record)
    return record


def low_stock_items(items: Inventory, threshold: int = LOW_STOCK_THRESHOLD) -> Inventory:
    """Return the items whose quantity is at or below ``threshold``."""
    return [item for item in items if item["quantity"] <= threshold]
