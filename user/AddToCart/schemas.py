from pydantic import BaseModel
from typing import Optional, Union, List
from admin.schemas import ProductSchemas
from datetime import date


class AddToCartSchemas(BaseModel):
    product_id : int
    quantity : int
  

class UpdateCartSchemas(BaseModel):
    item_id : int 
    quantity : int
  

class RemoveCartSchemas(BaseModel):
    item_id : int 

class CartDetailsSchemas(BaseModel):
    ordered : bool
    total_price : int
    created_at : date
    class Config():
        orm_mode = True

class CartItemsSchemas(BaseModel):
    # cart_details : CartDetailsSchemas 
    product_details : ProductSchemas
    quantity : int
    id : int
    class Config():
        orm_mode = True