"""JSON file storage (interim step).

The hard-coded list from v1.0 was exported to data/inventory.json; this
module reads and writes that file. It will be replaced by SQLite.
"""

import json

from .config import JSON_PATH
from .models import Item, ItemCreate, ItemUpdate


def _load() -> list[Item]:
    with open(JSON_PATH, encoding="utf-8") as f:
        rows = json.load(f)
    return [Item(id=i, **row) for i, row in enumerate(rows, start=1)]


def _save(items: list[Item]) -> None:
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump([i.model_dump(exclude={"id"}) for i in items], f, indent=2)


def list_items() -> list[Item]:
    return _load()


def get_item(item_id: int) -> Item | None:
    return next((i for i in _load() if i.id == item_id), None)


def create_item(data: ItemCreate) -> Item:
    items = _load()
    item = Item(id=len(items) + 1, **data.model_dump())
    _save(items + [item])
    return item


def update_item(item_id: int, data: ItemUpdate) -> Item | None:
    items = _load()
    for idx, item in enumerate(items):
        if item.id == item_id:
            items[idx] = item.model_copy(update=data.model_dump(exclude_unset=True))
            _save(items)
            return items[idx]
    return None


def delete_item(item_id: int) -> bool:
    items = _load()
    kept = [i for i in items if i.id != item_id]
    _save(kept)
    return len(kept) != len(items)
