from marshmallow import Schema, fields, validate
from marshmallow.decorators import post_load


class LoginRequestSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=50))

class LoginResponseSchema(Schema):
    message = fields.Str()
    auth_token = fields.Str()

class AuthorizationPayload:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role


class AuthorizationPayloadSchema(Schema):
    user_id = fields.Int(required=True)
    username = fields.Str(required=True)
    role = fields.Str(required=True)

    @post_load
    def make_payload(self, data, **kwargs):
        return AuthorizationPayload(**data)