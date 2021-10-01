from src.models.user import User
from src.models.product import Product


def add_users():
    User(
        username='user1',
        password='test',
        role='seller'
    ).save()

    User(
        username='user2',
        password='test',
        role='buyer',
        deposit=1500
    ).save()

    User(
        username='delete_me',
        password='test',
        role='buyer'
    ).save()


def add_products():
    Product(
        amount_available=100,
        cost=100,
        product_name='test_product_1',
        seller_id=1
    ).save()
    Product(
        amount_available=10,
        cost=200,
        product_name='test_product_2',
        seller_id=1
    ).save()
    Product(
        amount_available=10,
        cost=200,
        product_name='delete_me',
        seller_id=1
    ).save()
