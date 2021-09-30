from .. import db
from src.utils.mixins import CrudMixin


class Product(CrudMixin, db.Model):
    amount_available = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(128), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
