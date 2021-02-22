from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
import uuid
from infrastructure.flask_app import db


class ProductType(db.Model):
    __tablename__ = 'product_type'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String(50))


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    images = db.Column(JSON)
    price_value = db.Column(db.Float)
    price_currency = db.Column(db.String(5))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    product_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_type.id'))
    product_type = relationship("ProductType")
