from flask import Blueprint

product_blueprint = Blueprint('product', __name__)

from . import views

