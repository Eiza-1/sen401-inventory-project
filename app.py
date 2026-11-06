"""Inventory Manager demo application (v1.0).

Reads the items from inventory.py, calculates the total stock value and
prints a formatted stock report.  Run with:  python app.py
"""

from inventory import CURRENCY, LOW_STOCK_THRESHOLD, add_item, inventory, low_stock_items
from utils.helpers import highest_stock_item, item_value, lowest_stock_item

WIDTH = 52
LINE = "-" * WIDTH


def total_stock_value(items) -> float:
    """Return the total value of all stock (sum of quantity x price)."""
    return sum(item_value(item) for item in items)


def print_header() -> None:
    """Print the application title banner."""
    print("=" * WIDTH)
    print("            Inventory Manager v1.0")
    print("=" * WIDTH)


def print_stock_table(items) -> None:
    """Print each item with its quantity, unit price and line value."""
    print(f"{'Item':<14}{'Qty':>6}{'Unit Price':>14}{'Value':>18}")
    print(LINE)
    for item in items:
        print(f"{item['item_name']:<14}{item['quantity']:>6}"
              f"{item['price']:>14,.2f}{item_value(item):>18,.2f}")
    print(LINE)


def print_summary(items) -> None:
    """Print totals, highest/lowest stock and the low-stock alert."""
    high = highest_stock_item(items)
    low = lowest_stock_item(items)

    print(f"{'Total Items:':<24}{len(items)}")
    print(f"{'Total Units:':<24}{sum(i['quantity'] for i in items)}")
    print(f"{'Total Stock Value:':<24}{CURRENCY} {total_stock_value(items):,.2f}")
    if high and low:  # both are None when the list is empty
        print(f"{'Highest Stock:':<24}{high['item_name']} ({high['quantity']})")
        print(f"{'Lowest Stock:':<24}{low['item_name']} ({low['quantity']})")
    print(LINE)

    alerts = low_stock_items(items)
    names = ", ".join(i["item_name"] for i in alerts) if alerts else "none"
    print(f"Low-stock alert ({LOW_STOCK_THRESHOLD} or fewer): {names}")


def main() -> None:
    """Add a new item, then print the stock table and summary."""
    print_header()
    new = add_item("Webcam", 15, 25000)
    print(f"Added new item: {new['item_name']} ({new['quantity']} @ {CURRENCY} {new['price']:,})")
    print()
    print_stock_table(inventory)
    print_summary(inventory)


if __name__ == "__main__":
    main()
