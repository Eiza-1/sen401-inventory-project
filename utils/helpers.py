"""Reusable helper functions that work on any list of stock items."""


def item_value(item):
    """Return the stock value of one item (quantity x price)."""
    return item["quantity"] * item["price"]


def highest_stock_item(items):
    """Return the item with the largest quantity, or None if the list is empty."""
    if not items:
        return None
    return max(items, key=lambda i: i["quantity"])


def lowest_stock_item(items):
    """Return the item with the smallest quantity, or None if the list is empty."""
    if not items:
        return None
    return min(items, key=lambda i: i["quantity"])
