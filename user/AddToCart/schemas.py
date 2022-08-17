from pydantic import BaseModel
from typing import Optional, Union


class AddToCartSchemas(BaseModel):
    product_id : int 
    quantity : int
  

class UpdateCartSchemas(BaseModel):
    item_id : int 
    quantity : int
  

class RemoveCartSchemas(BaseModel):
    item_id : int 
  