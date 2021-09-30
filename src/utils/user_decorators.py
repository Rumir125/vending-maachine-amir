from functools import wraps
from http import HTTPStatus
from src.models.user import User
from src.models.product import Product

from flask import request
from .. import jwt

def is_role_valid(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                valid_roles = [role.value for role in allowed_roles]
                payload = jwt.decode(request.headers["Authorization"])
                if not payload:
                    return {"message": "You are not authorized"}, HTTPStatus.UNAUTHORIZED
            
                if payload.role in valid_roles:
                    return func(*args, **kwargs)
                else:
                    return {"messsage": f"User '{payload.username}' doesn't have valid role to perform this action."}, HTTPStatus.FORBIDDEN
            except:
                return {"message": "Something went wrong. Try again"}, HTTPStatus.INTERNAL_SERVER_ERROR
        return wrapper
    return decorator


def has_valid_seller(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = jwt.decode(request.headers["Authorization"])
        product_id = kwargs["product_id"]
        product = Product.get_by_id(product_id)
        if product is None:
            return {"":"Product doesn't exist"}, HTTPStatus.NOT_FOUND
        
        if payload and payload.user_id == product.seller_id:
            return func(*args, **kwargs)
        else:
            return {"message": f"Product Id doesn't belong to this user: {payload.user_id}"}, HTTPStatus.FORBIDDEN
    return wrapper

def does_user_exist(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs["user_id"]
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id: {user_id} doesn't exist"}, HTTPStatus.NOT_FOUND
        return func(*args, **kwargs)
    return wrapper
