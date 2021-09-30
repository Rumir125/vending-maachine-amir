from http import HTTPStatus

from flask_apispec.annotations import doc
from src.schemas.help_schemas import BaseResponseSchema
from src.schemas.auth_schemas import LoginRequestSchema, LoginResponseSchema
from flask import make_response
from flask_apispec.views import MethodResource
from flask_restful import Resource
from flask_apispec import use_kwargs, marshal_with
from src.services.auth_service import AuthService

@doc(tags=["Login"])
class LoginAuth(MethodResource, Resource):
    @use_kwargs(LoginRequestSchema, location=("json"))
    @marshal_with(
        LoginResponseSchema, code=HTTPStatus.OK, description="Login successful"
    )
    @marshal_with(
        BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Login forbidden"
    )
    @marshal_with(
        BaseResponseSchema,
        code=HTTPStatus.INTERNAL_SERVER_ERROR,
        description="Internal Server error",
    )
    def post(self, **kwargs):
        return AuthService.login_user(kwargs)
