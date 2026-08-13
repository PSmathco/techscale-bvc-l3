# TechScale: Test suite

from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
import order_service

client = TestClient(app)


# Pre-written — use this as a reference before writing your own tests below.
def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


# TODO: Check that the health endpoint returns a body with the expected fields.
def test_health_response_body():
    pass


# TODO: Check that the process endpoint accepts a valid payload and returns the expected status.
def test_process_returns_202():
    pass


# TODO: Call validate_order() directly with a valid quantity and assert it returns True.
# No database or HTTP call needed — this is a pure business logic test.
def test_validate_order_accepts_valid_quantity():
    pass


# TODO: Call validate_order() with an out-of-range quantity and assert it raises the correct error.
def test_validate_order_rejects_invalid_quantity():
    pass
