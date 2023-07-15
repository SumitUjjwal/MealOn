from flask import Blueprint
from controllers.admin import (
    add_dish,
    remove_dish,
    update_availability,
    update_order_status,
    review_all_orders
    )

# Create a new Blueprint instance
admin = Blueprint('admin', __name__)

# Defined Routes for the admin

@admin.route('/dish/add', methods=['POST'])
def add_dish_route():
    return add_dish()


@admin.route('/dish/remove/<dish_id>', methods=['DELETE'])
def remove_dish_route(dish_id):
    return remove_dish(dish_id)

@admin.route('/dish/update/<dish_id>/<quantity>', methods=['PATCH'])
def update_availability_route(dish_id, quantity):
    return update_availability(dish_id, quantity)

@admin.route('/orders/status/update', methods=['PATCH'])
def update_order_status_route():
    return update_order_status()

@admin.route('/orders', methods=['GET'])
def get_orders():
    return review_all_orders()