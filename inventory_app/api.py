"""REST API for the Inventory Manager (FastAPI).

Run locally:  uvicorn inventory_app.api:app --reload
Docs:         http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, status

from . import __version__, controllers
from .config import LOW_STOCK_THRESHOLD
from .models import Item, ItemCreate, ItemUpdate, StockSummary


@asynccontextmanager
async def lifespan(_: FastAPI):
    controllers.init_storage()  # create the database/table on startup
    yield


app = FastAPI(title="Inventory Manager API", version=__version__,
              description="SEN 401 Lab 4 - re-engineered Inventory Manager backed by SQLite.",
              lifespan=lifespan)


def _not_found(item_id: int) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} not found")


@app.get("/health", tags=["system"])
def health() -> dict:
    """Liveness check used by Docker Compose."""
    return {"status": "ok", "version": __version__}


@app.get("/items", response_model=list[Item], tags=["items"])
def list_items() -> list[Item]:
    """Return every item."""
    return controllers.list_items()


@app.get("/items/low-stock", response_model=list[Item], tags=["items"])
def low_stock(threshold: int = Query(LOW_STOCK_THRESHOLD, ge=0)) -> list[Item]:
    """Return items at or below the threshold."""
    return controllers.low_stock_items(threshold=threshold)


@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int) -> Item:
    """Return one item."""
    try:
        return controllers.get_item(item_id)
    except controllers.ItemNotFoundError:
        raise _not_found(item_id)


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item(data: ItemCreate) -> Item:
    """Create an item. Returns 409 if the name already exists."""
    try:
        return controllers.add_item(data)
    except controllers.DuplicateItemError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


@app.patch("/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, data: ItemUpdate) -> Item:
    """Change some fields of an item."""
    try:
        return controllers.update_item(item_id, data)
    except controllers.ItemNotFoundError:
        raise _not_found(item_id)
    except controllers.DuplicateItemError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int) -> None:
    """Delete an item."""
    try:
        controllers.remove_item(item_id)
    except controllers.ItemNotFoundError:
        raise _not_found(item_id)


@app.get("/summary", response_model=StockSummary, tags=["reports"])
def summary() -> StockSummary:
    """Totals, highest/lowest stock and low-stock items."""
    return controllers.stock_summary()
