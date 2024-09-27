from applications.database import db 
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    __tablename__ = "user"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    admin=db.Column(db.Boolean,nullable=False,default=False)

class Product(db.Model):
    __tablename__="products"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,unique=True,nullable=False)
    stock=db.Column(db.Integer,nullable=False)
    description=db.Column(db.String)
    availability=db.Column(db.String,nullable=False)
    mfg_date=db.Column(db.String,nullable=False)
    exp_date=db.Column(db.String,nullable=False)
    m_r_p=db.Column(db.Integer,nullable=False)
    type=db.Column(db.String,nullable=False)
    owner=db.Column(db.Integer,nullable=False)
    cat_id=db.Column(db.Integer,nullable=False)

class Category(db.Model):
    __tablename__="categories"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,unique=True,nullable=False)
    description=db.Column(db.String)
    owner=db.Column(db.Integer,nullable=False)

class Assets(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.Integer, nullable=False)
    customer = db.Column(db.Integer, nullable=False)
    product = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
