from pydantic import BaseModel
from typing import Optional, Union

class AdminSchemas(BaseModel):
    email : str
    first_name : str
    last_name : str
    password : str


class AdminLoginSchemas(BaseModel):
    email : str
    password : str


class UpdateAdminSchemas(BaseModel):
    first_name : str
    last_name : str


class CategorySchemas(BaseModel):
    catagory_name : str 

    class Config():
        orm_mode = True


class ProductSchemas(BaseModel):
    product_name : str
    description : str
    price : float
    is_available : bool
    catagory_id : CategorySchemas

    class Config():
        orm_mode = True

