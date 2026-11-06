def highest_stock_item(items):
    if not items:
        return None  # Corrective: avoid IndexError on an empty list
    best = items[0]
    for item in items:
        if item["quantity"] > best["quantity"]:
            best = item
    return best


def lowest_stock_item(items):
    if not items:
        return None  # Corrective: avoid IndexError on an empty list
    worst = items[0]
    for item in items:
        if item["quantity"] < worst["quantity"]:
            worst = item
    return worst
