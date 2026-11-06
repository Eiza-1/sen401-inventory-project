inventory = [
    {"item_name": "Laptop", "quantity": 10, "price": 450000},
    {"item_name": "Mouse", "quantity": 50, "price": 5000},
    {"item_name": "Keyboard", "quantity": 30, "price": 12000},
    {"item_name": "Monitor", "quantity": 8, "price": 150000},
    {"item_name": "USB Cable", "quantity": 100, "price": 1500},
]


def add_item(item_name, quantity, price):
    inventory.append({"item_name": item_name, "quantity": quantity, "price": price})
