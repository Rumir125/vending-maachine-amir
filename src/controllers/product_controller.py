from src.models.user import UserRolesEnum
from src.utils.user_decorators import has_valid_seller, is_role_valid
from .. import jwt
from src.schemas.help_schemas import BaseResponseSchema
from src.schemas.product_schemas import ProductResponseSchema, ProductSchema
from src.services.product_service import ProductService
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from http import HTTPStatus


@doc(tags=["Product"])
class ProductResourceList(MethodResource, Resource):

    @marshal_with(ProductSchema(many=True), code=HTTPStatus.OK, description="Products fetched")
    @marshal_with(ProductSchema, code=HTTPStatus.FORBIDDEN, description="Sorry, products can't be fetched!")
    def get(self):
        return ProductService.get_all_products()

    @jwt.check_token
    @is_role_valid(UserRolesEnum.SELLER)
    @use_kwargs(ProductSchema, location="json")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.CREATED, description="Product was successfully created")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Something went wrong. Product was not created")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.UNAUTHORIZED, description="You are not authorized to create products")
    def post(self, **kwargs):
        return ProductService.create_product(kwargs)


@doc(tags=["Product"])
class ProductResource(MethodResource, Resource):

    @marshal_with(ProductResponseSchema, code=HTTPStatus.OK, description="Product fetched")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="Product doesn't exist")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Something went wrong. Try again")
    def get(self, product_id):
        return ProductService.get_product(product_id)

    @jwt.check_token
    @is_role_valid(UserRolesEnum.SELLER)
    @has_valid_seller
    @use_kwargs(ProductSchema, location=("json"))
    @marshal_with(BaseResponseSchema, code=HTTPStatus.OK, description="Product updated successfully")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Something went wrong. Try again.")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="Product doesn't exist")
    def put(self, product_id, **kwargs):
        return ProductService.update_product(product_id, kwargs)

    
    @jwt.check_token
    @is_role_valid(UserRolesEnum.SELLER)
    @has_valid_seller
    @marshal_with(BaseResponseSchema, code=HTTPStatus.OK, description="Product successfully deleted")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description="Product doesn't exist")
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description="Something went wrong")
    def delete(self, product_id):
        return ProductService.delete_product(product_id)
