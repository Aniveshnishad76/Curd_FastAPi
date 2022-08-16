from pydantic import BaseModel
from typing import Optional, Union


class AddToCartSchemas(BaseModel):
    product_id : int 
    quantity : int
  