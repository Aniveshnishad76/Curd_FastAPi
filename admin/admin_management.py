from fastapi import FastAPI , Depends
import bcrypt
import model
from fastapi_jwt_auth import AuthJWT
from admin.schemas import AdminSchemas,AdminLoginSchemas,UpdateAdminSchemas,CategorySchemas,ProductSchemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List,Dict
from fastapi import APIRouter, Depends, HTTPException
from admin import schemas

router = APIRouter(
    prefix = '/admin',
    tags=["Admin-Management"]
)

model.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def set_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    password_hash = pwhash.decode('utf8')
    return password_hash


@router.post("/register")
def create_user(request: AdminSchemas, db : Session = Depends(get_db)):
    user = db.query(model.Admin).filter(model.Admin.email == request.email).first()
    if not user:
        hased_password = set_password(request.password)
        obj = model.Admin(first_name = request.first_name, last_name = request.last_name,email=request.email,hased_password = hased_password)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    else:
        return "User already exiest"

@router.post("/login")
def login_user(request: AdminLoginSchemas, db : Session = Depends(get_db),Authorize: AuthJWT = Depends()):
    data = db.query(model.Admin).filter(model.Admin.email == request.email).first()
    if data:
        check = check_password(request.password,data.hased_password)
        if check is True:
            access_token =  Authorize.create_access_token(subject=request.email)
            Authorize.set_access_cookies(access_token)
            return access_token
        else:
            return "Password not match"
    else:
        return "No email Exist"
    
@router.get("/profile")
def profile(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if user:
        data = db.query(model.Admin).filter(model.Admin.email == user).first()
        return data

@router.patch("/change_profile")
def change_profile(request: UpdateAdminSchemas,Authorize: AuthJWT = Depends(), db : Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if user:
        data = db.query(model.Admin).filter(model.Admin.email == user).first()
        data_for_change = request.dict(exclude_unset = True)
        for key, value in data_for_change.items():
            setattr(data,key,value)
        db.commit()
        data = db.query(model.Admin).filter(model.Admin.email == user).first()
        return data
    else:
        return "somthing went wrong"

    
@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return "Successfully logout"


@router.get('/catagory')
def get_categoery(db : Session = Depends(get_db)):
    data = db.query(model.Catagory).all()
    return data

@router.post('/catagory')
def create_categoery(request: CategorySchemas, db : Session = Depends(get_db)):
    data = model.Catagory(catagory_name = request.Catagory_name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@router.get('/products')#, response_model = ProductSchemas)
def get_all_product(db : Session = Depends(get_db)):
    data = db.query(model.Product).all()
    return data

@router.get('/products{product_id}' )       
def get_product_by_id(product_id : int , db : Session = Depends(get_db)):
    data = db.query(model.Product).filter(model.Product.id == product_id).first()
    return data

@router.post('/product')
def create_product(request: ProductSchemas, db : Session = Depends(get_db)):
    data = model.Product(product_name = request.product_name,description=request.description,price = request.price, catagory_id= request.catagory_id)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
