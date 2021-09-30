from src.controllers.product_controller import ProductResource, ProductResourceList
from src.controllers.user_controller import UserBuyResource, UserDepositResource, UserListResource, UserResetDepositResource, UserResource
from flask_restful import Api
from src.controllers.auth_controller import LoginAuth
from flask_apispec import FlaskApiSpec


def register_api_endpoints(api: Api):
    api.add_resource(LoginAuth, "/login")
    api.add_resource(UserListResource, "/users")
    api.add_resource(ProductResourceList, "/products")
    api.add_resource(UserDepositResource, "/deposit")
    api.add_resource(UserBuyResource, "/buy")
    api.add_resource(ProductResource, "/products/<product_id>" )
    api.add_resource(UserResource, "/users/<user_id>" )
    api.add_resource(UserResetDepositResource, "/reset_deposit" )


def register_docs(docs: FlaskApiSpec):
    docs.register(LoginAuth)
    docs.register(UserListResource)
    docs.register(ProductResourceList)
    docs.register(UserDepositResource)
    docs.register(UserBuyResource)
    docs.register(ProductResource)
    docs.register(UserResource)
    docs.register(UserResetDepositResource)
