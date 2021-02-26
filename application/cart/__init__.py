from flask import Blueprint

cart_blueprint = Blueprint('cart', __name__, url_prefix="/api")

from . import views
