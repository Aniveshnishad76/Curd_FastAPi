from fastapi import FastAPI , Depends
import bcrypt
import model
from fastapi_jwt_auth import AuthJWT
from user.schemas import UserSchemas,UserLoginSchemas,UpdateUserSchemas
from user.AddToCart.schemas import AddToCartSchemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

app = FastAPI(
    tags=["User-Add-To-Cart"]
)
router = APIRouter(
    tags=["User-Add-To-Cart"]
)

model.Base.metadata.create_all(bind=engine)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return Settings()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('Add-To-Cart')
def add_to_cart(request: AddToCartSchemas, db : Session = Depends(get_db)):
    pass
