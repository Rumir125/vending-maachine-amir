from http import HTTPStatus
from src.models.product import Product
from .. import jwt
from flask import request


class ProductService():

    @staticmethod
    def get_all_products():
        try:
            return Product.get_all()
        except:
            return {"message": "Something went wrong!. Users can't be fetched."}, HTTPStatus.FORBIDDEN

    def get_product(product_id):
        try:
            product = Product.query.filter_by(id=product_id).first()
            if product is None:
                return {"message":f"Product with id:{product_id} doesn't exist"}, HTTPStatus.NOT_FOUND
            return product
        except:
            return {"message":"Something went wrong. Please try again"}, HTTPStatus.FORBIDDEN

    @staticmethod
    def create_product(data_request):
        try:
            payload = jwt.decode(request.headers['Authorization'])
            product = Product(**data_request,seller_id=payload.user_id)
            product.save()
            product_name = data_request["product_name"]
            return {"message": f"Product {product_name} created"}, HTTPStatus.CREATED
        except:
            return {"message": "Something went wrong. Product was not created."}, HTTPStatus.FORBIDDEN

    @staticmethod
    def update_product(product_id, request_data):
        try:
            product = Product.query.filter_by(id=product_id).first()
   
            product.amount_available = request_data["amount_available"]
            product.product_name = request_data["product_name"]
            product.cost = request_data["cost"]
            product.save()

            return product, HTTPStatus.OK

        except:
            return {"message" : "Something went wrong. Try again"}, HTTPStatus.FORBIDDEN


    def delete_product(product_id):
        try:
            product = Product.query.filter_by(id=product_id).first()
            
            product.delete()
            return {"message":"Product was successfully deleted"}, HTTPStatus.OK
        except:
            return {"message": "Something went wrong. Try again"}, HTTPStatus.FORBIDDEN