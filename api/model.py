# from werkzeug.security import generate_password_hash, check_password_hash
# from marshmallow import Schema, fields

# class User:
#     '''Flask-Login requires a model in object form to login users
#     is_authenticated, is_active is plugged in from the mixin
#     '''
#     def __init__(self, first_name, last_name, email, password):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.password = self.hash_password(password)

#     def hash_password(self, password):
#         return generate_password_hash(password)
    
#     def check_hash(self, password):
#         return check_password_hash(User.password, password)


#     def get_fullname(self):
#         return self.first_name + ' ' + self.last_name
        

# class Template:
#     def __init__(self, name, subject, body, owner) -> None:
#         self.template_name = name
#         self.subject = subject
#         self.body = body
#         self.owner = owner


# class ObjectId(fields.Field):
#     def _serialize(self, value, attr, obj, **kwargs):
#         if value is None:
#             return ""
#         return "".join(str(d) for d in value)

#     def _deserialize(self, value, attr, data, **kwargs):
#         try:
#             return [int(c) for c in value]
#         except ValueError as error:
#             raise error


# class UserSchema(Schema):
#     _id = ObjectId()
#     first_name = fields.String()
#     last_name = fields.String()
#     email = fields.String()
#     password = fields.String()

# class TemplateSchema(Schema):
#     template_name = fields.String()
#     subject = fields.String()
#     body = fields.String()
#     owner = fields.Nested(UserSchema)


