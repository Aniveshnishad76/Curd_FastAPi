from pydantic import BaseModel
from typing import List


class OrdersSchemas(BaseModel):
    product_id : List[int] = []
    cart_id : int