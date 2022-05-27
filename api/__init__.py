import flask
from flask_restful import Api

import pymongo

import os
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv
load_dotenv()

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'sloovi-sloovin'

#JWT for assigning tokens for users
jwt = JWTManager(app)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')


#connect app to mongo db
mongo = pymongo.MongoClient(os.getenv('MONGO_URI'))

#get database and collection
db = pymongo.database.Database(mongo, 'sloovin')
col = pymongo.collection.Collection(db, 'users')

#instantiate flask-restful
api = Api(app)



from api import resources