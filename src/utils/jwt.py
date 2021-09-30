from http import HTTPStatus

from flask_apispec.annotations import doc
from src.schemas.auth_schemas import AuthorizationPayload, AuthorizationPayloadSchema
from functools import wraps
from flask import request
from flask.app import Flask
import jwt


class JWT():
    algorithm = 'HS256'

    def __init__(self, app: Flask = None):
        self.app = app

    def init_app(self, app: Flask):
        self.app = app

    def encode(self, payload) -> str:
        return jwt.encode(payload, self.app.config['JWT_SECRET_KEY'], self.algorithm)

    def decode(self, _jwt) -> AuthorizationPayload:
        return AuthorizationPayloadSchema().load(jwt.decode(_jwt, self.app.config['JWT_SECRET_KEY'], algorithms=[self.algorithm]))

    def check_token(self, func):
        @doc(
            security=[{
                "Authorization": []
            }]
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                payload = self.decode(request.headers['Authorization'])
                if payload:
                    return func(*args, **kwargs)
            except:
                pass
            return {
                "message": "Not Authorized"
            }, HTTPStatus.UNAUTHORIZED
        return wrapper
