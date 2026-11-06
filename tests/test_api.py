"""Tests for the FastAPI endpoints (needs fastapi + httpx)."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi.testclient import TestClient
except ImportError:  # pragma: no cover
    TestClient = None

from inventory_app import config  # noqa: E402


@unittest.skipIf(TestClient is None, "fastapi/httpx not installed")
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._old_db = config.DB_PATH
        config.DB_PATH = Path(self.tmp.name) / "api.db"
        from inventory_app.api import app
        self.client = TestClient(app)
        self.client.__enter__()  # runs the lifespan (creates tables)

    def tearDown(self):
        self.client.__exit__(None, None, None)
        config.DB_PATH = self._old_db
        self.tmp.cleanup()

    def test_health(self):
        self.assertEqual(self.client.get("/health").json()["status"], "ok")

    def test_full_crud_flow(self):
        r = self.client.post("/items", json={"item_name": "Laptop", "quantity": 10, "price": 450000})
        self.assertEqual(r.status_code, 201)
        item_id = r.json()["id"]

        self.assertEqual(len(self.client.get("/items").json()), 1)
        self.assertEqual(self.client.get(f"/items/{item_id}").json()["item_name"], "Laptop")

        r = self.client.patch(f"/items/{item_id}", json={"quantity": 4})
        self.assertEqual(r.json()["quantity"], 4)
        self.assertEqual(self.client.get("/summary").json()["total_value"], 1_800_000)
        self.assertEqual(len(self.client.get("/items/low-stock").json()), 1)

        self.assertEqual(self.client.delete(f"/items/{item_id}").status_code, 204)
        self.assertEqual(self.client.get(f"/items/{item_id}").status_code, 404)

    def test_validation_and_conflict(self):
        bad = self.client.post("/items", json={"item_name": "", "quantity": -1, "price": 1})
        self.assertEqual(bad.status_code, 422)
        self.client.post("/items", json={"item_name": "Mouse", "quantity": 1, "price": 1})
        dup = self.client.post("/items", json={"item_name": "Mouse", "quantity": 1, "price": 1})
        self.assertEqual(dup.status_code, 409)


if __name__ == "__main__":
    unittest.main()
