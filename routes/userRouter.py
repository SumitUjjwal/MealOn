from flask import Blueprint
from controllers.user import place_order
from controllers.admin import get_menu
from middleware.authenticator import token_required

# Create a new Blueprint instance
user = Blueprint('user', __name__)

# Defined Routes for the user
# Get menu
@user.route('/menu', methods=['GET'])
def get_menu_route():
    return get_menu()

# Place order
@user.route('/orders/place', methods=['POST'])
@token_required
def place_order_route():
    return place_order()