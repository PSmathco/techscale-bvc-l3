# TechScale: Business logic layer
# Pricing rules and order validation only — no database or HTTP imports here.
# If a change is driven by a pricing policy or business rule, it belongs here.
# If it is driven by a schema change or HTTP contract, it belongs elsewhere.

def validate_order(quantity: int) -> bool:
    """Validate an order quantity according to business rules."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if quantity > 1000:
        raise ValueError("Cannot order more than 1000 units")

    return True


def calculate_price(product_id: int, quantity: int) -> float:
    """Calculate the total order price based on the product tier."""
    if product_id <= 0:
        raise ValueError("Product ID must be positive")

    if product_id < 100:
        unit_price = 9.99
    elif product_id < 200:
        unit_price = 24.99
    else:
        unit_price = 49.99

    return round(quantity * unit_price, 2)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== validate_order ===")
    print(validate_order(5))           # True
    try:
        validate_order(-1)
    except ValueError as e:
        print(f"Caught: {e}")
    try:
        validate_order(1500)
    except ValueError as e:
        print(f"Caught: {e}")

    print("\n=== calculate_price ===")
    print(calculate_price(50, 3))      # 29.97
    print(calculate_price(150, 2))     # 49.98
    print(calculate_price(250, 1))     # 49.99
    try:
        calculate_price(-5, 1)
    except ValueError as e:
        print(f"Caught: {e}")