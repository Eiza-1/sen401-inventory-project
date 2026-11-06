"""SQLite persistence layer.

All SQL lives here, so the rest of the application never needs to know how
or where data is stored.
"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

from . import config
from .models import Item, ItemCreate, ItemUpdate

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name   TEXT    NOT NULL UNIQUE,
    quantity    INTEGER NOT NULL CHECK (quantity >= 0),
    price       REAL    NOT NULL CHECK (price >= 0),
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class DuplicateItemError(ValueError):
    """Raised when an item with the same name already exists."""


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    """Open a connection, commit on success, roll back on error, always close."""
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create the database file and the items table if they do not exist."""
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.executescript(SCHEMA)


def _to_item(row: sqlite3.Row) -> Item:
    return Item(id=row["id"], item_name=row["item_name"],
                quantity=row["quantity"], price=row["price"])


def list_items() -> list[Item]:
    with connect() as conn:
        rows = conn.execute("SELECT id, item_name, quantity, price FROM items ORDER BY id").fetchall()
    return [_to_item(r) for r in rows]


def get_item(item_id: int) -> Item | None:
    with connect() as conn:
        row = conn.execute("SELECT id, item_name, quantity, price FROM items WHERE id = ?",
                           (item_id,)).fetchone()
    return _to_item(row) if row else None


def create_item(data: ItemCreate) -> Item:
    try:
        with connect() as conn:
            cur = conn.execute("INSERT INTO items (item_name, quantity, price) VALUES (?, ?, ?)",
                               (data.item_name, data.quantity, data.price))
            new_id = cur.lastrowid
    except sqlite3.IntegrityError as e:
        raise DuplicateItemError(f"Item '{data.item_name}' already exists") from e
    return Item(id=new_id, **data.model_dump())


def update_item(item_id: int, data: ItemUpdate) -> Item | None:
    changes = data.model_dump(exclude_unset=True, exclude_none=True)
    if changes:
        # Column names come from the Pydantic model, never from user input
        assignments = ", ".join(f"{col} = ?" for col in changes)
        try:
            with connect() as conn:
                conn.execute(f"UPDATE items SET {assignments} WHERE id = ?",
                             (*changes.values(), item_id))
        except sqlite3.IntegrityError as e:
            raise DuplicateItemError(f"Item '{changes.get('item_name')}' already exists") from e
    return get_item(item_id)


def delete_item(item_id: int) -> bool:
    with connect() as conn:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    return cur.rowcount > 0
