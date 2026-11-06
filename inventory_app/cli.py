"""Console interface (presentation layer only - no business logic here).

Usage:
    python app.py                      # print stock report
    python app.py add "Webcam" 15 25000
    python app.py low-stock
    python app.py --api http://localhost:8000   # report via the REST API

If --api (or the INVENTORY_API_URL environment variable) is set, the report
is fetched over HTTP from the FastAPI service instead of the local database.
This is how the 'report' container talks to the 'api' container.
"""

import argparse
import json
import os
import urllib.request

from pydantic import ValidationError

from . import controllers
from .models import Item, ItemCreate, StockSummary
from .utils import format_money, item_value

WIDTH = 60
LINE = "-" * WIDTH


def print_stock_table(items: list[Item]) -> None:
    """Print every item with quantity, unit price and line value."""
    print(f"{'ID':<4}{'Item':<14}{'Qty':>6}{'Unit Price':>14}{'Value':>18}")
    print(LINE)
    for i in items:
        print(f"{i.id:<4}{i.item_name:<14}{i.quantity:>6}{i.price:>14,.2f}{item_value(i):>18,.2f}")
    print(LINE)


def print_summary(s: StockSummary) -> None:
    """Print the summary statistics."""
    print(f"{'Total Items:':<24}{s.total_items}")
    print(f"{'Total Units:':<24}{s.total_units}")
    print(f"{'Total Stock Value:':<24}{format_money(s.total_value, s.currency)}")
    if s.highest_stock and s.lowest_stock:
        print(f"{'Highest Stock:':<24}{s.highest_stock.item_name} ({s.highest_stock.quantity})")
        print(f"{'Lowest Stock:':<24}{s.lowest_stock.item_name} ({s.lowest_stock.quantity})")
    print(LINE)
    names = ", ".join(i.item_name for i in s.low_stock) or "none"
    print(f"Low-stock alert ({s.low_stock_threshold} or fewer): {names}")


def _get_json(url: str):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.load(resp)


def report(api_url: str | None = None) -> None:
    """Print the full stock report, from the API if ``api_url`` is given."""
    print("=" * WIDTH)
    print("                Inventory Manager v2.0")
    print("=" * WIDTH)
    if api_url:
        print(f"Source: REST API {api_url}")
        items = [Item(**i) for i in _get_json(f"{api_url}/items")]
        summary = StockSummary(**_get_json(f"{api_url}/summary"))
    else:
        print("Source: local SQLite database")
        items, summary = controllers.list_items(), controllers.stock_summary()
    print_stock_table(items)
    print_summary(summary)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="inventory", description="Inventory Manager v2.0")
    parser.add_argument("--api", default=os.getenv("INVENTORY_API_URL"),
                        help="base URL of the REST API (report only)")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("report", help="print the stock report (default)")
    add = sub.add_parser("add", help="add a new item")
    add.add_argument("item_name")
    add.add_argument("quantity", type=int)
    add.add_argument("price", type=float)
    sub.add_parser("low-stock", help="list items that need re-ordering")
    args = parser.parse_args(argv)
    if args.api and args.command in (None, "report"):
        report(args.api.rstrip("/"))
        return 0
    controllers.init_storage()

    if args.command == "add":
        try:
            item = controllers.add_item(ItemCreate(item_name=args.item_name,
                                                   quantity=args.quantity, price=args.price))
        except ValidationError as e:
            print("Invalid item:", "; ".join(err["msg"] for err in e.errors()))
            return 1
        except controllers.DuplicateItemError as e:
            print("Error:", e)
            return 1
        print(f"Added item #{item.id}: {item.item_name} ({item.quantity} @ {format_money(item.price)})")
    elif args.command == "low-stock":
        for i in controllers.low_stock_items():
            print(f"{i.item_name}: {i.quantity}")
    else:
        report()
    return 0
