from pydantic import BaseModel
from typing import Optional, Union

class AddToCartSchemas(BaseModel):
    User : int
    Catagory : int
    quantity : int
    price : str
    cart : str
  