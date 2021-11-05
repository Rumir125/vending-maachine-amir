from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    amount_available = fields.Int(validate=validate.Range(min=0))
    cost = fields.Int()
    product_name = fields.Str()
    id = fields.Int()


class ProductResponseSchema(Schema):
    id = fields.Int()
    amount_available = fields.Int(validate=validate.Range(min=0))
    cost = fields.Int()
    product_name = fields.Str()
    seller_id = fields.Int()