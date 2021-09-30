from .. import db, bcrypt, jwt
from enum import Enum
from src.utils.mixins import CrudMixin

class UserRolesEnum(Enum):
    BUYER = "buyer"
    SELLER = "seller"


class User(CrudMixin, db.Model):
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    deposit = db.Column(db.Float, default=0.0)
    role = db.Column(
        db.Enum(*[role.value for role in UserRolesEnum], name="user_roles_enum"),
        default="buyer",
    )
    products = db.relationship("Product", backref="user", lazy=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_access_token(self):
        return {
            "message": f"Welcome {self.username}",
            "auth_token": jwt.encode(
                {
                    "user_id": self.id,
                    "username": self.username,
                    "role": self.role
                }
            )
        }
