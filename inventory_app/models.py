"""Data models (the 'M' layer).

Pydantic models replace the hand-written isinstance() checks from v1.0:
the rules are declared once and reused by the CLI, the API and the database.
"""

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt


class ItemBase(BaseModel):
    """Fields shared by every representation of a stock item."""

    model_config = ConfigDict(str_strip_whitespace=True)

    item_name: str = Field(min_length=1, max_length=100, examples=["Laptop"])
    quantity: StrictInt = Field(ge=0, examples=[10])
    price: StrictFloat | StrictInt = Field(ge=0, examples=[450000])


class ItemCreate(ItemBase):
    """Data required to create a new item."""


class ItemUpdate(BaseModel):
    """Partial update - only the fields that are sent are changed."""

    model_config = ConfigDict(str_strip_whitespace=True)

    item_name: str | None = Field(default=None, min_length=1, max_length=100)
    quantity: StrictInt | None = Field(default=None, ge=0)
    price: StrictFloat | StrictInt | None = Field(default=None, ge=0)


class Item(ItemBase):
    """A stored item, identified by a unique id."""

    id: int


class StockSummary(BaseModel):
    """Aggregated statistics for the whole inventory."""

    currency: str
    total_items: int
    total_units: int
    total_value: float
    highest_stock: Item | None
    lowest_stock: Item | None
    low_stock_threshold: int
    low_stock: list[Item]
