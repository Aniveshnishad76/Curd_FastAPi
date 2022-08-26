from fastapi import FastAPI , Depends, status, Response
import bcrypt
import model
import random
from fastapi_jwt_auth import AuthJWT
from user.schemas import UserSchemas,UserLoginSchemas,UpdateUserSchemas
from user.AddToCart.schemas import AddToCartSchemas,UpdateCartSchemas,RemoveCartSchemas
from user.UserOrder.schemas import OrdersSchemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

app = FastAPI(
    tags=["User-Order"]
)
router = APIRouter(
    tags=["User-Order"]
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


@router.get("/my-orders" )
def my_orders(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if user:
        data = db.query(model.Orders).filter(model.Orders.user == user , model.Orders.is_paid == True).all()
        if data:
            dict = []
            for i in data:
                for j in i.products:
                    result = db.query(model.Product).filter(model.Product.id == j).first()
                    if result:
                        dict.append(result)
                i.products = dict   
            return data
        else:
            return "NO order Found"

@router.post("/order", status_code =200)
def order(response : Response, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    order_id = "ORDER_ID_" + str(random.randint(1000, 9999))
    payment_id = "PAYMENT_ID_" + str(random.randint(1000, 9999))
    try:
        cart = db.query(model.Cart).filter(model.Cart.user == user).first()
        cart_items = db.query(model.CartItems).filter(model.CartItems.user == user,model.CartItems.cart == cart.id).all()
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "No item in bag"
    product_ids = []
    for i in cart_items:
        product_ids.append(i.products)
    data = model.Orders(user = user,cart = cart.id ,price =cart.total_price,products =product_ids,is_paid=True, order_id = order_id,payment_id=payment_id)
    db.add(data)
    db.commit()
    db.refresh(data)
    result = db.query(model.CartItems).filter(model.CartItems.user == user).delete()
    db.commit()
    db.query(model.Cart).filter(model.Cart.user == user).delete()
    db.commit()
    return "Order success"
