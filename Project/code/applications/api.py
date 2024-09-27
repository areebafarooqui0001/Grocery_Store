from flask_restful import Resource, fields, marshal_with, request, reqparse
from applications.models import User, Product, Category
from applications.database import db
from applications.validation import BusinessValidationError, NotFoundError, DuplicationError, NotAuthorizedError
import secrets
import os
import datetime as dt
from applications.config import api


products_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "stock": fields.Integer,
    "description": fields.String,
    "availability": fields.String,
    "mgf_date": fields.String,
    "exp_date": fields.String,
    "m_r_p": fields.Integer,
    "type": fields.Integer,
    "owner": fields.Integer,
    "cat_id": fields.Integer
    }

#--------------api for products--------------

parser=reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('stock')
parser.add_argument('description')
parser.add_argument('availability')
parser.add_argument('mfg_date')
parser.add_argument('exp_date')
parser.add_argument('m_r_p')
parser.add_argument('type')


class Api_Product(Resource):
    #--------------create product--------------
    def post(self):
        info=parser.parse_args()
        new_product=Product(name=info['name'],
            stock=info['stock'],
            description=info['description'],
            avaiability=info['availability'],
            mfg_date=info['mfg_date'],
            exp_date=info['exp_date'],
            m_r_p=info['m_r_p'],
            type=info['type'])
        db.session.add(new_product)
        db.session.commit()
        return { "status":"product created"},201
    
    #--------------read product--------------
    
    def get(self):
        all_products={}
        products=Product.query.all()
        for product in products:
            all_products[product.id]=product.name
        return all_products
    
    #-------------update product---------------
    def put(self,id):
        info=parser.parse_args()
        p_update=Product.query.get(id)
        p_update.name=info['name']
        p_update.stock=info['stock']
        p_update.description=info['description']
        p_update.availability=info['availability']
        p_update.mrp_date=info['mfg_date']
        p_update.exp_date=info['exp_date']
        p_update.m_r_p=info['m_r_p']
        p_update.type=info['type']
        db.session.commit()
        return { "status":"product updated"},201
    
    #-------------delete product---------------
    def delete(self,id):
        p_del=Product.query.get(id)
        db.session.delete(p_del)
        db.session.commit()
        return {"status":"product deleted"},202
    
#------------api endpoints for products--------------
api.add_resource(Api_Product,"/api/create_product","/api/all_products","/api/update_products/<int:id>","/api/delete_product/<int:id>")


categories_fields ={
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "owner": fields.Integer,
}

#-----------api for categories-------------
parser.add_argument('name')
parser.add_argument('description')

class Api_Category(Resource):
    #-----------create category--------------
    def post(self):
        info=parser.parse_args()
        new_category = Category(
            name=info['name'],
            description=info['description']
        )
        db.session.add(new_category)
        db.session.commit()
        return { "status":"category created"},201
    

    #------------read category---------------
    def get(self):
        all_categories={}
        categories=Category.query.all()
        for cat in categories:
            all_categories[cat.id]=cat.name
        return all_categories
    
    #-------------update category-------------
    def put(self,id):
        info=parser.parse_args()
        c_update=Category.query.get(id)
        c_update.name=info['name']
        c_update.description=info['description']
        
        db.session.commit()
        return { "status":"category updated"},201
    
    #-------------delete category---------------
    def delete(self,id):
        c_del=Category.query.get(id)
        db.session.delete(c_del)
        db.session.commit()
        return {"status":"category deleted"},202
    
#-------------api endpoints for category------------------
api.add_resource(Api_Category,"/api/create_category","/api/all_categories","/api/update_category/<int:id>","/api/delete_category/<int:id>")
