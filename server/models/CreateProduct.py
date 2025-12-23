from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    quantity: int = Field(..., ge=0)
    price: Decimal = Field(..., gt=0)
