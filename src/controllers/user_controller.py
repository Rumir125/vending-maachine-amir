from src.models.user import UserRolesEnum
from src.utils.user_decorators import does_user_exist, is_role_valid
from src.schemas.help_schemas import BaseResponseSchema
from src.schemas.user_schemas import DepositRequestSchema, RegistrationRequestSchema, RegistrationResponseSchema, UserBuyRequestSchema, UserBuyResponseSchema, UserResponseSchema, UserSchema, UserUpdateRequestSchema
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import use_kwargs, marshal_with, doc
from src.services.user_service import UserService
from http import HTTPStatus
from .. import jwt
from flask import request


@doc(tags=["User"])
class UserListResource(MethodResource, Resource):
    @marshal_with(
        UserSchema(many=True), code=HTTPStatus.OK, description="Users fetched"
    )
    @marshal_with(
        UserSchema, code=HTTPStatus.FORBIDDEN, description="Request forbidden"
    )
    def get(self):
        return UserService.get_users()

    @use_kwargs(RegistrationRequestSchema, location=("json"))
    @marshal_with(RegistrationResponseSchema, code=HTTPStatus.CREATED, description="User was created")
    @marshal_with(RegistrationResponseSchema, code=HTTPStatus.CONFLICT, description="Username already exists")
    @marshal_with(RegistrationResponseSchema, code=HTTPStatus.FORBIDDEN, description="Something went wrong and user was not created")
    def post(self, **kwargs):
        return UserService.create_user(kwargs)

    
@doc(tags=["User"])
class UserDepositResource(MethodResource, Resource):


    @jwt.check_token
    @is_role_valid(UserRolesEnum.BUYER)
    @use_kwargs(DepositRequestSchema, location=("json"))
    @marshal_with(BaseResponseSchema, code=HTTPStatus.OK, description="User deposit added ")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="User not found ")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Something went wrong. Try again.")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.BAD_REQUEST, description="Invalid deposit value")
    def post(self, **kwargs):
        return UserService.deposit(kwargs)



@doc(tags=["User"])
class UserBuyResource(MethodResource, Resource):

    @jwt.check_token
    @is_role_valid(UserRolesEnum.BUYER)
    @use_kwargs(UserBuyRequestSchema, location=("json"))
    @marshal_with(UserBuyResponseSchema, code=HTTPStatus.OK, description="Product bought successfully")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Something went wrong. Please try again")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="Product doesn't exist")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.BAD_REQUEST, description="You don't have enough money or or request amount is not available")
    def post(self, **kwargs):
        return UserService.buy_product(kwargs)


@doc(tags=["User"])
class UserResource(MethodResource, Resource):

    @jwt.check_token
    @does_user_exist
    @marshal_with(UserResponseSchema, code=HTTPStatus.OK, description="User was found")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="User doesn't exist")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Somehing went wrong.")
    def get(self, user_id):
        return UserService.get_user(user_id)

    @jwt.check_token
    @does_user_exist
    @use_kwargs(UserUpdateRequestSchema, location=("json"))
    @marshal_with(UserResponseSchema, code=HTTPStatus.OK, description="User was updated")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="User doesn't exist")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Somehing went wrong.")
    def put(self, user_id, **kwargs):
        return UserService.update_user(user_id, kwargs)

    @jwt.check_token
    @does_user_exist
    @marshal_with(BaseResponseSchema, code=HTTPStatus.OK, description="User was deleted successfully")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="User doesn't exist")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Somehing went wrong.")
    def delete(self, user_id):
        return UserService.delete_user(user_id)
    
@doc(tags=["User"])
class UserResetDepositResource(MethodResource, Resource):

    @jwt.check_token
    @is_role_valid(UserRolesEnum.BUYER)
    @marshal_with(BaseResponseSchema, code=HTTPStatus.OK, description="User reset deposit successfully")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="User doesn't exist")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Somehing went wrong.")
    def patch(self):
        payload = jwt.decode(request.headers["Authorization"])
        return UserService.reset_deposit(payload.user_id)