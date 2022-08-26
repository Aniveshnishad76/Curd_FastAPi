from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.dialects.postgresql import BIGINT,ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, time, timedelta
from typing import List

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
    products = relationship('Product', back_populates= 'catagory')

class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key = True, index = True)
    product_name = Column(String)
    description = Column(String)
    price = Column(Float, default=0)
    is_available = Column(Boolean, default= True)
    catagory_id = Column(Integer,ForeignKey('Catagory.id'))
    catagory = relationship('Catagory', back_populates= 'products')
    cart_items = relationship('CartItems', back_populates= 'product_details')


class Cart(Base):
    __tablename__ = 'Cart'
    id = Column(Integer, primary_key = True, index = True)
    user = Column(String)
    ordered = Column(Boolean,default=False)
    total_price = Column(Float,default=0)
    created_at = Column(DateTime,default = datetime.now())
    cartitem = relationship('CartItems', back_populates= 'cart_details')


class CartItems(Base):
    __tablename__ = 'CartItems'
    id = Column(Integer, primary_key = True, index = True)
    user = Column(String)
    cart = Column(Integer,ForeignKey('Cart.id'))
    products = Column(Integer,ForeignKey('Product.id'))
    price = Column(Float,default=0)
    quantity = Column(Integer,default=1)
    cart_details = relationship('Cart', back_populates= 'cartitem')
    product_details = relationship('Product', back_populates= 'cart_items')


class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key = True, index = True)
    user = Column(String)
    cart = Column(Integer)
    products =  Column(ARRAY(Integer),nullable = False)
    price = Column(Float,default=0)
    is_paid = Column(Boolean,default=False)
    payment_id = Column(String)
    order_id = Column(String)
