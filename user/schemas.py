from pydantic import BaseModel
from typing import Optional, Union

class UserSchemas(BaseModel):
    email : str
    first_name : str
    last_name : str
    password : str
    
class UserLoginSchemas(BaseModel):
    email : str
    password : str

class UpdateUserSchemas(BaseModel):
    first_name : str
    last_name : str