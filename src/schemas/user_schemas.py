from marshmallow import Schema, fields, validate
from src.models.user import UserRolesEnum


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    role = fields.Str(validate=validate.OneOf([e.value for e in UserRolesEnum]))
    deposit = fields.Int()


class RegistrationResponseSchema(Schema):
    auth_token = fields.Str()
    message = fields.Str()


class RegistrationRequestSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    role = fields.Str(validate=validate.OneOf([e.value for e in UserRolesEnum]))

class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    role = fields.Str(validate=validate.OneOf([e.value for e in UserRolesEnum]))
    deposit = fields.Int()


class DepositRequestSchema(Schema):
    user_id = fields.Int()
    deposit = fields.Int()


class UserBuyRequestSchema(Schema):
    amount = fields.Int(required=True, validate=validate.Range(min=1))
    product_id = fields.Int(required=True)

class UserBuyResponseSchema(Schema):
    money_spent = fields.Int()
    product_id = fields.Int()
    message = fields.Str()
    money_left = fields.Int()
    amount_bought = fields.Int()

class UserUpdateRequestSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    role = fields.Str(validate=validate.OneOf([e.value for e in UserRolesEnum]))