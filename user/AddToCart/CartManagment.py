from fastapi import FastAPI , Depends, status, Response
import bcrypt
import model
from fastapi_jwt_auth import AuthJWT
from user.schemas import UserSchemas,UserLoginSchemas,UpdateUserSchemas
from user.AddToCart.schemas import AddToCartSchemas,UpdateCartSchemas,RemoveCartSchemas,CartItemsSchemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
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


@router.get('/My-Cart',response_model = List[CartItemsSchemas])
def my_cart(response : Response, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if user:
        cart_item = db.query(model.CartItems).filter(model.CartItems.user == user).all()
        return cart_item
    else:
        response.status_code = status.HTTP_404_CONTENT_NOT_FOUND
        return "Your cart is empty"
    

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
    
    check = db.query(model.CartItems).filter(model.CartItems.user == user,model.CartItems.products == request.product_id).all()
    if check:
        return "Already in cart"
    else:
        total_price = 0
        result = model.CartItems(user = user,cart=cart[0].id,products = request.product_id , price = (product[0].price)*(request.quantity) ,quantity = request.quantity)
        db.add(result)
        db.commit()
        db.refresh(result)
        cart_items = db.query(model.CartItems).filter(model.CartItems.user == user, model.CartItems.cart ==cart[0].id ).all()
        for items in cart_items:
            total_price = total_price + items.price

        dict1 = { 'total_price' : total_price }
        for key, value in dict1.items():
            setattr(cart[0],key,value)
        db.commit()
        return "Added in cart"


@router.patch('/Update-Cart')
def update_cart_items(request:UpdateCartSchemas,Authorize: AuthJWT = Depends(), db : Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if user:
        cart_items = db.query(model.CartItems).filter(model.CartItems.id == request.item_id,model.CartItems.user == user).all()
        product_id = cart_items[0].products
        products_details = db.query(model.Product).filter(model.Product.id == product_id).all()
        price = products_details[0].price
        new_price = price * request.quantity 
        dict1 = { 'quantity' : request.quantity , 'price' : new_price }
        for key, value in dict1.items():
            setattr(cart_items[0],key,value)
        db.commit()

        cart = db.query(model.Cart).filter(model.Cart.user == user, model.Cart.ordered == False).all()
        cart_item = db.query(model.CartItems).filter(model.CartItems.user == user).all()
        total_price = 0
        for items in cart_item:
            total_price = total_price + items.price

        dict1 = { 'total_price' : total_price }
        for key, value in dict1.items():
            setattr(cart[0],key,value)
        db.commit()
        return "Updated"

@router.delete('/Remove-from-cart')
def remove_from_cart(request:RemoveCartSchemas,Authorize: AuthJWT = Depends(), db : Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if user:
        db.query(model.CartItems).filter(model.CartItems.id == request.item_id,model.CartItems.user == user).delete()
        
        cart = db.query(model.Cart).filter(model.Cart.user == user, model.Cart.ordered == False).all()
        
        cart_items = db.query(model.CartItems).filter(model.CartItems.user == user).all()
        
        total_price = 0
        for items in cart_items:
            total_price = total_price + items.price

        dict1 = { 'total_price' : total_price }
        for key, value in dict1.items():
            setattr(cart[0],key,value)
        db.commit()

        return "Item deleted"

# @router.get('/testing')
# def Testing( db : Session = Depends(get_db)):
#     result = db.query(model.Catagory).order_by(model.Catagory.catagory_name).all()
#     return result 
        
    
