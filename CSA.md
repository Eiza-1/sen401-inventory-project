# Configuration Status Accounting (CSA) – Inventory Manager

Configuration Status Accounting records **what** changed, **who** changed it, **when**, **why**, and **which baseline** each change belongs to. This file is the CSA record for Lab 3. The raw Git data is exported in `changelog.txt`.

## 1. Configuration items

| Item | Type | Description |
|------|------|-------------|
| `inventory.py` | Source | Item data (`item_name`, `quantity`, `price`), validation and low-stock check |
| `app.py` | Source | Calculates total stock value and prints the stock report |
| `utils/helpers.py` | Source | `item_value()`, `highest_stock_item()`, `lowest_stock_item()` |
| `tests/test_inventory.py` | Test | 8 unit tests |
| `requirements.txt` | Config | Python 3.12+, standard library only |
| `README.md`, `CSA.md`, `changelog.txt` | Docs | Project, status accounting and change log documents |

## 2. Branches

| Branch | Purpose | Status |
|--------|---------|--------|
| `main` | Stable / released code | Contains release `v1.0` (merge commit `c97532d`) |
| `dev`  | All maintenance work before release | Fully merged into `main` |

## 3. Releases / baselines

| Tag | Commit | Date | Contents |
|-----|--------|------|----------|
| `v1.0` | `c97532d` | 2026-11-06 | Initial code + all four maintenance tasks, merged from `dev` |

## 4. Commit-to-maintenance-task mapping

| Commit | Branch | Maintenance type | Change | Files |
|--------|--------|------------------|--------|-------|
| `cc32f55` | main | – (initial) | README and .gitignore | README.md, .gitignore |
| `dc65af8` | main | – (initial) | Inventory data module | inventory.py |
| `0390e20` | main | – (initial) | Highest/lowest stock helpers | utils/ |
| `ef10171` | main | – (initial) | App with total stock value | app.py, requirements.txt |
| `48a6b10` | dev | **Corrective** | Total value used price only (643,500) – fixed to quantity × price (6,835,000); empty-list IndexError fixed | app.py, utils/helpers.py |
| `a7df335` | dev | **Adaptive** | Python 3.12 typing (`type` alias, TypedDict); new `validate_item()` and `low_stock_items()` | inventory.py, README.md, requirements.txt |
| `e99adaf` | dev | **Perfective** | Formatted table, line values, thousands separators, low-stock alert | app.py |
| `dc453ab` | dev | **Preventive** | Docstrings, constants, `item_value()` helper (DRY), smaller functions, unit tests | inventory.py, app.py, utils/helpers.py, tests/ |
| `98715e3` | dev | Documentation | README updated with maintenance summary | README.md |
| `c97532d` | main | Release | Merge `dev` → `main`, tagged `v1.0` | – |

## 5. Commands used for status accounting

```bash
git log --oneline                       # short commit list
git log --graph --oneline --all         # branch structure
git log --pretty=format:"%h | %an | %ad | %s" --date=iso   # commits, authors, dates
git branch -a -v                        # all branches and their latest commit
git tag -n                              # releases with messages
git log --stat --oneline                # files changed per commit
git log --all --pretty=format:"%h | %an | %ad | %d %s" --date=iso > changelog.txt
```

## 6. Observations

- Using a type prefix in every commit message (`fix(corrective)`, `feat(adaptive)`, `feat(perfective)`, `refactor(preventive)`) makes it possible to trace each maintenance task straight from `git log`.
- Doing all maintenance on `dev` and merging with `--no-ff` keeps a visible branch in `git log --graph`, so it is clear which commits made up the release.
- The `v1.0` tag freezes the exact configuration that was released, so it can always be rebuilt with `git checkout v1.0`.
