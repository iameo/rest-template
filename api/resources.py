import flask
from flask_restful import Resource

from werkzeug.security import generate_password_hash, check_password_hash

from bson.json_util import dumps

from api import api, col, jwt


from api.utils import fetch_json, fetch_identity_if_logged_on

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from bson.objectid import ObjectId

# import re
from email_validator import validate_email, EmailNotValidError

'''All required resources in this module, a better design would to have each in a separate module, for readability'''


'''return current user via token validation'''
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


'''check if you are a logged on user'''
class CheckAuth(Resource):
    def get(self):
        user = fetch_identity_if_logged_on()
        if user:
            return flask.jsonify(message="logged on")
        return flask.jsonify(message="not logged on")



class Login(Resource):
    def post(self):
        '''post methodview for generating access token if provided data is valid'''

        _json = fetch_json()

        email = _json["email"]
        password = _json["password"]

        user = col.find_one({"email":email})
        if user:
            password_check = check_password_hash(user["password"], password)
            if password_check:
                access_token = create_access_token(identity=email)
                return flask.jsonify(access_token=access_token, message="plug in ypur access token for access")
            return flask.jsonify(message="incorrect password!")
        return flask.jsonify(message="user does not exist")



class Register(Resource):
    def post(self):
        '''post methodview for the creation of users'''

        _json = fetch_json()

        first_name = _json["first_name"]
        last_name = _json["last_name"]
        password = _json["password"]
        email = _json["email"]

        try:
            email = validate_email(email).email
        except EmailNotValidError as e:
            return flask.jsonify(message=str(e))
            
        if first_name and last_name and password and email:
            if not col.find_one({"email":email}):
                '''stored hashed value of password as password'''
                hashed_pwd = generate_password_hash(password)
                col.insert_one({"email":email, "password": hashed_pwd, "first_name":first_name, "last_name":last_name})
                return flask.jsonify(status=201, message="user registered successfully")
            return flask.jsonify(message="email already registered!")
        return flask.jsonify(status=400, message="missing credentials")


class Template(Resource):
    @jwt_required()
    def get(self, template_id):
        current_user = get_jwt_identity()

        '''fetch template if name exists and is owned by current user'''
        template = col.find_one({"_id": ObjectId(template_id), "owner":current_user})
        if template:
            return flask.jsonify(message="template found", data=dumps(template), status=200)
        return flask.jsonify(message="template does not exist in your repository", status=404)

    @jwt_required()
    def put(self, template_id):
        current_user = get_jwt_identity()

        _json = fetch_json()

        template_name = _json["template_name"]
        body = _json["body"]
        subject = _json["subject"]

        '''fetch template if name exists and is owned by current user'''
        template = col.find_one({"_id": ObjectId(template_id), "owner":current_user})
        if template:
            col.update_one({"_id":ObjectId(template_id)}, {"$set":{"template_name":template_name, "body":body, "subject":subject}})
            return flask.jsonify(message="template updated", status=200)
        return flask.jsonify(message="template does not exist in your repository", status=404)

    @jwt_required()
    def delete(self, template_id):
        current_user = get_jwt_identity()

        '''fetch template if name exists and is owned by current user'''
        template = col.find_one({"_id": ObjectId(template_id), "owner":current_user})
        if template:
            col.delete_one({"_id":ObjectId(template_id)})
            return flask.jsonify(message="template deleted", status=200)
        return flask.jsonify(message="template does not exist in your repository", status=404)


class CreateTemplate(Resource):
    @jwt_required()
    def get(self):
        '''get templates of current user'''
        templates_by_owner = col.find({"owner": get_jwt_identity()})
        return flask.jsonify(data=dumps(templates_by_owner), status=200)

    @jwt_required()
    def post(self):
        _json = fetch_json()

        template_name = _json["template_name"]
        subject = _json["subject"]
        body = _json["body"]

        if template_name and subject and body:
            '''insert to collection with new field owner: current_user'''
            col.insert_one({"template_name":template_name, "subject": subject, "body":body, "owner":get_jwt_identity()})
            return flask.jsonify(status=201, message="template created successfully")
        return flask.jsonify(status=400, message="missing credentials")


class HelloSloovi(Resource):
    def get(self):
        return flask.jsonify(
            database="MongoDB",
            web_framework="Flask",
            Limited_authorized_access="Yes",
            app_type="Rest API",
            documentation="https://github.com/iameo/rest-template/",
            message="sloovin....")

api.add_resource(CheckAuth, '/check-auth')
api.add_resource(Register, '/register') #endpoint 1
api.add_resource(Login, '/login') #endpoint 2
api.add_resource(Template, '/template/<template_id>') #endpoint 3(a)
api.add_resource(CreateTemplate, '/template') #endpoint 3(b)
api.add_resource(HelloSloovi, '/')