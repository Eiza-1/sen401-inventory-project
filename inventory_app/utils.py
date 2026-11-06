"""Small, pure helper functions shared by every layer (DRY)."""

from collections.abc import Iterable

from .config import CURRENCY
from .models import ItemBase


def item_value(item: ItemBase) -> float:
    """Return the stock value of one item (quantity x price)."""
    return item.quantity * item.price


def total_value(items: Iterable[ItemBase]) -> float:
    """Return the combined value of all items."""
    return sum(item_value(i) for i in items)


def format_money(amount: float, currency: str = CURRENCY) -> str:
    """Format an amount as e.g. 'NGN 6,835,000.00'."""
    return f"{currency} {amount:,.2f}"
