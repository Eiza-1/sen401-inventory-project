"""Entry point for the Inventory Manager v2.0 console interface.

All logic now lives in the inventory_app package; see docs/REVERSE_ENGINEERING.md.
"""

import sys

from inventory_app.cli import main

if __name__ == "__main__":
    sys.exit(main())
