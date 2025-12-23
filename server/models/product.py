#models/product.py
from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    product_name: str
    description: str
    quantity: int
    price: float

    model_config = {
        "from_attributes": True
    }