"""Central configuration. Values can be overridden with environment variables
so the same code runs locally and inside Docker containers."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CURRENCY = os.getenv("INVENTORY_CURRENCY", "NGN")
LOW_STOCK_THRESHOLD = int(os.getenv("INVENTORY_LOW_STOCK", "10"))

# Legacy data file (source for the migration)
JSON_PATH = Path(os.getenv("INVENTORY_JSON", BASE_DIR / "data" / "inventory.json"))

# SQLite database used from v2.0 onwards
DB_PATH = Path(os.getenv("INVENTORY_DB", BASE_DIR / "data" / "inventory.db"))
