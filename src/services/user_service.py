from src.models.product import Product
from typing import Union
from src.models.user import User
from http import HTTPStatus
from .. import jwt
from flask import request


class UserService:
    allowed_coins = [100, 50, 20, 10, 5]

    @staticmethod
    def get_users():
        try:
            return User.get_all()
        except:
            return {"messsage": "Something went wrong"}, HTTPStatus.FORBIDDEN

    @staticmethod
    def get_user_by_username(username: str) -> Union[User, None]:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def check_if_user_exists(username):
        return User.query.filter_by(username=username).first() is not None

    @staticmethod
    def create_user(login_request):
        try:
            if UserService.check_if_user_exists(login_request["username"]):
                return {"messsage": "Username already exists"}, HTTPStatus.CONFLICT

            user = User(**login_request)
            user.save()
            return user.generate_access_token(), HTTPStatus.CREATED
        except:
            return {"message": "Something went wrong"}, HTTPStatus.FORBIDDEN

    @staticmethod
    def deposit(deposit_request):
        try:
            payload = jwt.decode(request.headers["Authorization"])
            user_id = payload.user_id
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return {"message": f"User with id: {user_id} doesn't exist"}, HTTPStatus.NOT_FOUND

            if not deposit_request["deposit"] in UserService.allowed_coins:
                return {"message": f"Only {', '.join([str(coin) for coin in UserService.allowed_coins])} coins allowed"}, HTTPStatus.CONFLICT
            
            user.deposit =  user.deposit + deposit_request["deposit"]
            user.save()
            return {"message":"User deposit set successfully"}, HTTPStatus.OK

        except:
            return {"message": "Something went wrong"}, HTTPStatus.FORBIDDEN

    @staticmethod
    def buy_product(buy_request):
        try:
            payload = jwt.decode(request.headers["Authorization"])
            product_id = buy_request["product_id"]
            product = Product.query.filter_by(id=product_id).first()
            if product is None:
                return {"message": f"Product with id:{product_id} doesn't exist"}, HTTPStatus.NOT_FOUND
            
            
            user = User.query.filter_by(id=payload.user_id).first()
            if user is None:
                return{"message":"User was not found"}, HTTPStatus.NOT_FOUND

            amount = buy_request["amount"]

            if product.amount_available < amount:
                return {"message" : f"There is less than {amount} products available"}, HTTPStatus.CONFLICT

            total_cost = product.cost * buy_request["amount"]
            if total_cost > user.deposit:
                return {"message" : "You don't have enough money in deposit to buy a product"}, HTTPStatus.CONFLICT

            user.deposit = user.deposit - total_cost
            user.save()
            product.amount_available = product.amount_available - amount
            product.save()

            return {
                "money_spent": total_cost,
                "product_id": product.id,
                "message":"You  bought a product successfully",
                "money_left": user.deposit,
                "amount_bought" : amount,
                "change": UserService.calculate_change(user.deposit)}, HTTPStatus.OK,
        except:
            return {"message": "Something went wrong. Please try again"}, HTTPStatus.FORBIDDEN

    @staticmethod
    def get_user(user_id):
        try:
            user = User.get_by_id(user_id)
            return user, HTTPStatus.OK
        except:
            return {"message":" Something went wrong. Try again"}, HTTPStatus.FORBIDDEN

    @staticmethod
    def update_user(user_id, request_data):
        try:
            user = User.query.filter_by(id=user_id).first()

            username = request_data["username"]
            duplicate_user = User.query.filter_by(username=username).first()
            if user.username != username and duplicate_user:
                return {"message":"Username already taken"}, HTTPStatus.CONFLICT
            user.update(**request_data)

            return user, HTTPStatus.OK
        except:
            return {"message":" Something went wrong. Try again"}, HTTPStatus.FORBIDDEN

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.get_by_id(user_id)
            user.delete()
            return {"message": "User was deleted successfully"}, HTTPStatus.OK
        except:
            return {"message":" Something went wrong. Try again"}, HTTPStatus.FORBIDDEN

    @staticmethod
    def reset_deposit(user_id):
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return {"message": f"User with id:{user_id} doesn't exist"}, HTTPStatus.NOT_FOUND
            user.deposit = 0
            user.save()
            return {"message": "User deposit was reset successfully"}, HTTPStatus.OK
        except:
            return {"message":" Something went wrong. Try again"}, HTTPStatus.FORBIDDEN

    def calculate_change(total_amount):
        change = []
        for coin in UserService.allowed_coins:
            amount = (total_amount // coin)
            total_amount -= (total_amount // coin) * coin
            change.append({"amount": amount, "coin": coin})
        return change
