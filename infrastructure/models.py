from infrastructure.flask_app import db
from sqlalchemy.dialects.postgresql import JSON


class ProductType(db.Model):
    __tablename__ = 'product_type'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50))


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    images = db.Column(JSON)
    product_type_id = db.Column(db.String, db.ForeignKey('product_type.id'), nullable=False)
    price_value = db.Column(db.Integer)
    price_currency = db.Column(db.String(5))
