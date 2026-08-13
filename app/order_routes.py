# TechScale: HTTP routing layer
# Route handlers receive HTTP input, delegate to the service and repository layers, and return responses.
# No pricing logic, validation rules, or SQL belongs in this file.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import order_service
import order_repository

router = APIRouter()


class OrderCreate(BaseModel):
    customer_id: str
    product_id: int
    quantity: int


@router.post("/orders")
async def create_order(order: OrderCreate):
    """Validate and price an order through the service layer."""
    try:
        order_service.validate_order(order.quantity)
        total_price = order_service.calculate_price(
            order.product_id,
            order.quantity,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {
        "total_price": total_price,
        "status": "pending",
    }


@router.get("/orders/top")
async def get_top_orders():
    """Return the top orders through the repository layer."""
    orders = order_repository.get_top_orders()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    return orders