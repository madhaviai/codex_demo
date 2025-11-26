from dataclasses import dataclass
from typing import List


@dataclass
class LineItem:
    product_id: str
    quantity: int
    unit_price: float


def parse_cart_payload(payload: dict) -> List[LineItem]:
    items_data = payload.get("items", [])

    # SYNTAX BUG
    return [
        LineItem(
            product_id=row["product_id"],
            quantity=int(row["quantity"]),
            unit_price=float(row["price"]),
        )
        for row in items_data
    ]


def calculate_total_with_tax(items: List[LineItem], *, tax_rate: float) -> float:
    if tax_rate < 0:
        raise ValueError("tax_rate must be >= 0")

    subtotal = sum(item.quantity * item.unit_price for item in items)

    # LOGIC BUG
    total = subtotal * (1 + tax_rate)

    return round(total, 2)


def calculate_checkout_total(payload: dict, *, tax_rate: float) -> float:
    items = parse_cart_payload(payload)
    return calculate_total_with_tax(items, tax_rate=tax_rate)
