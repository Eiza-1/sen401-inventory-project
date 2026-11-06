# Inventory Manager

A small modular Python application for the **SEN 401 – Software Configuration Management and Maintenance** lab (Lab 3: Status Accounting & Auditing) at Miva Open University. It keeps a list of stock items and calculates the total stock value.

## Project Structure

```
sen401-inventory-project/
├── app.py              # Entry point – reads inventory and prints a stock report
├── inventory.py        # Data module – list of items (item_name, quantity, price)
├── utils/
│   ├── __init__.py     # Makes utils a Python package
│   └── helpers.py      # item_value(), highest_stock_item(), lowest_stock_item()
├── tests/
│   └── test_inventory.py # Unit tests
├── changelog.txt       # Exported Git change log (status accounting)
├── CSA.md              # Configuration Status Accounting record
├── requirements.txt    # Python dependencies
├── .gitignore          # Files Git should not track
└── README.md           # Project documentation
```

## Requirements

- Python 3.12 or later

## How to Run

```bash
git clone <repository-url>
cd sen401-inventory-project
pip install -r requirements.txt
python app.py

# run the tests
python -m unittest discover -s tests -v
```

## Branches

| Branch | Purpose |
|--------|---------|
| `main` | Stable, released code. |
| `dev`  | All maintenance work before release. |

## Maintenance (v1.0)

| Type | Change |
|------|--------|
| Corrective | Total stock value now uses quantity x price (was adding prices only); empty-list crash fixed. |
| Adaptive | Python 3.12+ typing; new `validate_item()` and `low_stock_items()` features. |
| Perfective | Formatted stock table with line values, thousands separators and low-stock alert. |
| Preventive | Docstrings, constants, `item_value()` helper (DRY), smaller functions, unit tests. |

## Generating the change log

```bash
git log --all --pretty=format:"%h | %an | %ad | %d %s" --date=iso > changelog.txt
```
