from fastapi import FastAPI , Depends
import bcrypt
import model
from fastapi_jwt_auth import AuthJWT
from user.schemas import UserSchemas,UserLoginSchemas,UpdateUserSchemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

app = FastAPI(
    tags=["User-Management"]
)
router = APIRouter(
    tags=["User-Management"]
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


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def set_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    password_hash = pwhash.decode('utf8')
    return password_hash


@router.post("/register")
def create_user(request: UserSchemas, db : Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == request.email).first()
    if not user:
        hased_password = set_password(request.password)
        obj = model.User(first_name = request.first_name, last_name = request.last_name,email=request.email,hased_password = hased_password)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    else:
        return "User already exiest"

@router.post("/login")
def login_user(request: UserLoginSchemas, db : Session = Depends(get_db),Authorize: AuthJWT = Depends()):
    data = db.query(model.User).filter(model.User.email == request.email).first()
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
        data = db.query(model.User).filter(model.User.email == user).first()
        return data

@router.patch("/change_profile")
def change_profile(request: UpdateUserSchemas,Authorize: AuthJWT = Depends(), db : Session = Depends(get_db)):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if user:
        data = db.query(model.User).filter(model.User.email == user).first()
        data_for_change = request.dict(exclude_unset = True)
        for key, value in data_for_change.items():
            setattr(data,key,value)
        db.commit()
        data = db.query(model.User).filter(model.User.email == user).first()
        return data
    else:
        return "somthing went wrong"

    
@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return "Successfully logout"