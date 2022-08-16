from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key = True, index = True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique = True, index= True)
    hased_password = Column(String)
    is_active = Column(Boolean, default = True)


class Admin(Base):
    __tablename__ = 'Admin'

    id = Column(Integer, primary_key = True, index = True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique = True, index= True)
    hased_password = Column(String)
    is_active = Column(Boolean, default = True)

class Catagory(Base):
    __tablename__ = 'Catagory'

    id = Column(Integer, primary_key = True, index = True)
    catagory_name = Column(String, unique=True)
    products = relationship('Product', back_populates= 'catagory_in')

class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key = True, index = True)
    product_name = Column(String)
    description = Column(String)
    price = Column(Float, default=0)
    is_available = Column(Boolean, default= True)
    catagory_id = Column(Integer,ForeignKey('Catagory.id'))
    catagory_in = relationship('Catagory', back_populates= 'products')

