import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.billing_service import (
    LineItem,
    parse_cart_payload,
    calculate_total_with_tax,
    calculate_checkout_total,
)


def test_parse_cart_payload_creates_line_items():
    payload = {
        "items": [
            {"product_id": "BOOK-001", "quantity": 2, "price": 15.99},
            {"product_id": "PEN-002", "quantity": "1", "price": "2.50"},
        ]
    }

    items = parse_cart_payload(payload)
    assert len(items) == 2


def test_calculate_total_with_tax():
    items = [
        LineItem("LAPTOP-123", 1, 1000.00),
        LineItem("MOUSE-456", 2, 50.00),
    ]

    total = calculate_total_with_tax(items, tax_rate=0.15)
    assert total == 1265.0


def test_calculate_checkout_total_rounding():
    payload = {
        "items": [
            {"product_id": "GUM-111", "quantity": 1, "price": 0.3333},
        ]
    }

    total = calculate_checkout_total(payload, tax_rate=0.0)
    assert total == 0.33
