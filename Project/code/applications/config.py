from flask import Flask
from flask_restful import Api
DB = "sqlite:///./instance/database.sqlite3"

app=Flask(__name__,template_folder='templates',static_folder='static')
api=Api(app)