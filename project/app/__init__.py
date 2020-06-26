from flask import flask
from app import routes
from flask_pymongo import PyMongo

import os 

file_path = os.path.abspath(os.getcwd())+"/todo.db"

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)