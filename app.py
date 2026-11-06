from inventory import inventory, add_item
from utils.helpers import highest_stock_item, lowest_stock_item


def total_stock_value(items):
    total = 0
    for item in items:
        total += item["quantity"] * item["price"]  # Corrective: value = quantity x price
    return total


def main():
    print("=== Inventory Manager ===")
    print()

    print("Items in stock:")
    for item in inventory:
        print(item["item_name"], "-", item["quantity"], "@", item["price"])
    print()

    add_item("Webcam", 15, 25000)
    print("Added new item: Webcam (15 @ 25000)")
    print()

    high = highest_stock_item(inventory)
    low = lowest_stock_item(inventory)

    print("Total Items:", len(inventory))
    print("Total Stock Value:", total_stock_value(inventory))
    print("Highest Stock:", high["item_name"], high["quantity"])
    print("Lowest Stock:", low["item_name"], low["quantity"])


if __name__ == "__main__":
    main()
