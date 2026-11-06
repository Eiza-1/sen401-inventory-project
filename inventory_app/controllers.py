"""Business logic (the 'C' layer).

Every interface (CLI, REST API) calls these functions; none of them talk to
storage directly. This removes the v1.0 problem of logic living in app.py.
"""

from . import database as repo
from .database import DuplicateItemError  # noqa: F401  (re-exported for callers)
from .config import CURRENCY, LOW_STOCK_THRESHOLD
from .models import Item, ItemCreate, ItemUpdate, StockSummary
from .utils import total_value


class ItemNotFoundError(LookupError):
    """Raised when an item id does not exist."""


def init_storage() -> None:
    """Make sure the database and its tables exist."""
    repo.init_db()


def list_items() -> list[Item]:
    """Return all items."""
    return repo.list_items()


def get_item(item_id: int) -> Item:
    """Return one item or raise ItemNotFoundError."""
    item = repo.get_item(item_id)
    if item is None:
        raise ItemNotFoundError(item_id)
    return item


def add_item(data: ItemCreate) -> Item:
    """Store a new item (already validated by the model).

    Raises:
        DuplicateItemError: If an item with the same name exists.
    """
    return repo.create_item(data)


def update_item(item_id: int, data: ItemUpdate) -> Item:
    """Change some fields of an item."""
    item = repo.update_item(item_id, data)
    if item is None:
        raise ItemNotFoundError(item_id)
    return item


def remove_item(item_id: int) -> None:
    """Delete an item."""
    if not repo.delete_item(item_id):
        raise ItemNotFoundError(item_id)


def low_stock_items(items: list[Item] | None = None,
                    threshold: int = LOW_STOCK_THRESHOLD) -> list[Item]:
    """Return items whose quantity is at or below ``threshold``."""
    items = list_items() if items is None else items
    return [i for i in items if i.quantity <= threshold]


def stock_summary(items: list[Item] | None = None,
                  threshold: int = LOW_STOCK_THRESHOLD) -> StockSummary:
    """Calculate totals, highest/lowest stock and low-stock items in one place."""
    items = list_items() if items is None else items
    return StockSummary(
        currency=CURRENCY,
        total_items=len(items),
        total_units=sum(i.quantity for i in items),
        total_value=total_value(items),
        highest_stock=max(items, key=lambda i: i.quantity, default=None),
        lowest_stock=min(items, key=lambda i: i.quantity, default=None),
        low_stock_threshold=threshold,
        low_stock=low_stock_items(items, threshold),
    )
