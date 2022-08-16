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


@router.post('/Add-To-Cart')
def add_to_cart(request: AddToCartSchemas,Authorize: AuthJWT = Depends(), db : Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    cart = db.query(model.Cart).filter(model.User.email == model.Cart.user, model.Cart.ordered == False).all()
    if len(cart) < 1:
        cart_update = model.Cart(user = user,ordered = False)
        db.add(cart_update)
        db.commit()
        db.refresh(cart_update)
    cart = db.query(model.Cart).filter(model.User.email == model.Cart.user, model.Cart.ordered == False).all()
    product = db.query(model.Product).filter(model.Product.id == request.product_id).all()
    result = model.CartItems(user = user,cart=cart[0].id,products = request.product_id , price = product[0].price,quantity = request.quantity)
    
    data = db.query(model.Cart).filter(model.User.email == user, model.Cart.ordered == False).first()
    data.total_price = request.quantity * product[0].price
    db.commit()

    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.get('/My-Cart')
def my_cart(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if user:
        data = db.query(model.Cart).filter(model.Cart.user == user, model.Cart.ordered == False).first()
        return data
    
