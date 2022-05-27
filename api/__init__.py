from email import message
import flask
from flask_restful import Api

import pymongo

import os
from flask_jwt_extended import JWTManager

from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'sloovi-sloovin'

CORS(app)
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

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return flask.jsonify(message="Token expired, even last week's milk taste better"), 401

@jwt.unauthorized_loader
def my_invalid_token_callback(expired_token):
    return flask.jsonify(message="unauthorized! request token"), 401