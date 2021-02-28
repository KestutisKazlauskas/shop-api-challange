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
    product_type = relationship("ProductType", lazy="joined", join_depth=1)


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'))
    product_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_type.id'))
    cart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cart.id'))
    product_name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    free_unit_price = db.Column(db.Float)
    currency = db.Column(db.String(5))


class Discount(db.Model):
    __tablename__ = 'cart_discount'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    cart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cart.id'), primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    currency = db.Column(db.String(5))


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    total = db.Column(db.Float)
    currency = db.Column(db.String(5))
    items = db.relationship('CartItem', backref='cart_item', lazy="joined", join_depth=1)
    discounts = db.relationship('Discount', backref='cart_discount', lazy="joined", join_depth=1)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('order.id'))
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    cart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cart.id'), primary_key=True)
    items = db.relationship('OrderItem', backref='order_item', lazy="joined", join_depth=1)
    customer_name = db.Column(db.String(255))
    customer_surname = db.Column(db.String(255))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    postal_code = db.Column(db.String(255))
    total = db.Column(db.Float)
    discount = db.Column(db.Float)
    currency = db.Column(db.String(5))
    status = db.Column(db.String(20))

