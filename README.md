# Inventory Manager

A small modular Python application for the **SEN 401 – Software Configuration Management and Maintenance** lab (Lab 3: Status Accounting & Auditing) at Miva Open University. It keeps a list of stock items and calculates the total stock value.

## Project Structure

```
sen401-inventory-project/
├── app.py              # Entry point – reads inventory and prints a stock report
├── inventory.py        # Data module – list of items (item_name, quantity, price)
├── utils/
│   ├── __init__.py     # Makes utils a Python package
│   └── helpers.py      # highest_stock_item(), lowest_stock_item()
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
```

## Branches

| Branch | Purpose |
|--------|---------|
| `main` | Stable, released code. |
| `dev`  | All maintenance work before release. |
