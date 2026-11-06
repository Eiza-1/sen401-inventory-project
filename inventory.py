from typing import TypedDict


class Item(TypedDict):
    item_name: str
    quantity: int
    price: float


# Python 3.12+ type alias statement (PEP 695)
type Inventory = list[Item]

inventory: Inventory = [
    {"item_name": "Laptop", "quantity": 10, "price": 450000},
    {"item_name": "Mouse", "quantity": 50, "price": 5000},
    {"item_name": "Keyboard", "quantity": 30, "price": 12000},
    {"item_name": "Monitor", "quantity": 8, "price": 150000},
    {"item_name": "USB Cable", "quantity": 100, "price": 1500},
]


def validate_item(item_name: str, quantity: int, price: float) -> Item:
    # Adaptive maintenance: new validation feature (standard library only)
    if not isinstance(item_name, str) or not item_name.strip():
        raise ValueError("Item name must be a non-empty string")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
        raise ValueError("Quantity must be a whole number of 0 or more")
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        raise ValueError("Price must be a number of 0 or more")
    return {"item_name": item_name.strip(), "quantity": quantity, "price": price}


def add_item(item_name: str, quantity: int, price: float) -> None:
    inventory.append(validate_item(item_name, quantity, price))


def low_stock_items(items: Inventory, threshold: int = 10) -> Inventory:
    # Adaptive maintenance: new feature - list items that need re-ordering
    return [item for item in items if item["quantity"] <= threshold]
