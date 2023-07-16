from flask import Blueprint
from controllers.user import place_order
from middleware.authenticator import token_required

# Create a new Blueprint instance
user = Blueprint('user', __name__)

# Defined Routes for the user
# Place order
@user.route('/orders/place', methods=['POST'])
@token_required
def place_order_route():
    return place_order()