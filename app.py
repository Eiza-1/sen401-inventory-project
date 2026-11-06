from inventory import inventory, add_item, low_stock_items
from utils.helpers import highest_stock_item, lowest_stock_item

LINE = "-" * 52


def total_stock_value(items):
    total = 0
    for item in items:
        total += item["quantity"] * item["price"]  # Corrective: value = quantity x price
    return total


def main():
    print("=" * 52)
    print("            Inventory Manager v1.0")
    print("=" * 52)

    add_item("Webcam", 15, 25000)
    print("Added new item: Webcam (15 @ NGN 25,000)")
    print()

    print(f"{'Item':<14}{'Qty':>6}{'Unit Price':>14}{'Value':>18}")
    print(LINE)
    for item in inventory:
        value = item["quantity"] * item["price"]
        print(f"{item['item_name']:<14}{item['quantity']:>6}"
              f"{item['price']:>14,.2f}{value:>18,.2f}")
    print(LINE)

    total = total_stock_value(inventory)
    units = sum(item["quantity"] for item in inventory)
    high = highest_stock_item(inventory)
    low = lowest_stock_item(inventory)

    print(f"{'Total Items:':<24}{len(inventory)}")
    print(f"{'Total Units:':<24}{units}")
    print(f"{'Total Stock Value:':<24}NGN {total:,.2f}")
    if high and low:
        print(f"{'Highest Stock:':<24}{high['item_name']} ({high['quantity']})")
        print(f"{'Lowest Stock:':<24}{low['item_name']} ({low['quantity']})")
    print(LINE)

    alerts = low_stock_items(inventory)
    print("Low-stock alert (10 or fewer):",
          ", ".join(i["item_name"] for i in alerts) if alerts else "none")


if __name__ == "__main__":
    main()
