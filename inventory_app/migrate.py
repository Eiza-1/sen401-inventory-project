"""Data migration: legacy JSON file -> SQLite database.

Usage:  python -m inventory_app.migrate [--json PATH]

The migration is idempotent: items that already exist (same item_name) are
skipped, so it is safe to run every time the containers start.
"""

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from . import config, database
from .models import ItemCreate


def migrate(json_path: Path) -> tuple[int, int, int]:
    """Copy every valid record from ``json_path`` into SQLite.

    Returns:
        (migrated, skipped_existing, rejected_invalid)
    """
    database.init_db()
    with open(json_path, encoding="utf-8") as f:
        rows = json.load(f)

    migrated = skipped = rejected = 0
    for row in rows:
        try:
            item = ItemCreate(**row)
        except ValidationError as e:
            rejected += 1
            print(f"  REJECTED {row}: {e.errors()[0]['msg']}")
            continue
        try:
            database.create_item(item)
            migrated += 1
            print(f"  migrated  {item.item_name}")
        except database.DuplicateItemError:
            skipped += 1
            print(f"  skipped   {item.item_name} (already in database)")
    return migrated, skipped, rejected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate inventory JSON to SQLite")
    parser.add_argument("--json", type=Path, default=config.JSON_PATH)
    args = parser.parse_args(argv)

    print(f"Migrating {args.json} -> {config.DB_PATH}")
    migrated, skipped, rejected = migrate(args.json)
    total = len(database.list_items())
    print(f"Done: {migrated} migrated, {skipped} skipped, {rejected} rejected. "
          f"Items in database: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
