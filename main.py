from fastapi import FastAPI , Depends
import bcrypt
from user import user_management
from user.AddToCart import CartManagment
from admin import admin_management
import model
from fastapi_jwt_auth import AuthJWT
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


app.include_router(user_management.router)
app.include_router(admin_management.router)
app.include_router(CartManagment.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

