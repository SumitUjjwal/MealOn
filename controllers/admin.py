# - Exit the system.

from flask import jsonify, request, abort
from models.db import users, orders, menu
from bson.objectid import ObjectId
from pymongo import errors

# View the Menu
def get_menu():
    try:
        menuList = list(menu.find({}))

        # Convert ObjectId instances to strings
        for dish in menuList:
            dish['_id'] = str(dish['_id'])
   
        return jsonify({'OK': True, 'Menu': menuList}), 200

    except Exception as e:
        return jsonify({'OK': False, 'error': 'An unexpected error occurred'}), 500

# - Add a new dish to the menu.
def add_dish():
    try:
        dish = request.get_json()
        title = dish.get('title')
        description = dish.get('description')
        price = dish.get('price')
        quantity = dish.get('quantity')
        availability = dish.get('availability')

        if not dish:
            abort(400, "Invalid JSON Data")

        checkExiting = menu.find_one({'title': title})
        if checkExiting:
            return jsonify({'OK': False, 'error': 'Dish already exists'}), 400
        else: 
            menu.insert_one(dish)
            return jsonify({'OK': True, 'message': 'Dish added successfully'}), 201
    except errors.PyMongoError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

# - Remove a dish no longer served.
def remove_dish(id):
    try:
        dish_id = ObjectId(id)
        res = menu.delete_one({'_id': dish_id})
        
        if res.deleted_count > 0:
            return jsonify({'OK': True, 'message': f'Dish with id: {id} removed successfully'}), 200
        else:
            return jsonify({'OK': False, 'message': f'Dish with id: {id} does not exist'}), 404
    except Exception as e:
        return jsonify({'OK': False, 'message': f'Error: {str(e)}'}), 500
     
# - Update the availability of a dish.
def update_availability(id, quantity):
    try:
        dish_id = ObjectId(id)
        res = menu.update_one({'_id': dish_id}, {'$set': {'quantity': quantity}})
        if res.modified_count > 0:
            return jsonify({'OK': True, 'message': f'Dish with id: {id} updated successfully'}), 200
        else:
            return jsonify({'OK': False, 'message': f'Dish with id: {id} does not exist'}), 404
    except errors.PyMongoError as e:
        return jsonify({'OK': False, 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'OK': False, 'message': 'An unexpected error occurred'}), 500

# - Update the status of an order.
# Valid order statuses
VALID_STATUSES = {'order placed', 'accepted', 'rejected', 'preparing', 'pickedup', 'delivered'}

# Function to update the status of an order
def update_order_status():
    try:
        data = request.get_json()
        order_id = data.get('orderid')
        new_status = data.get('status')

        # Validate the new status
        if new_status not in VALID_STATUSES:
            return jsonify({'OK': False, 'error': 'Invalid status'}), 400

        order_id = ObjectId(order_id)

        # Check if the order exists in the database
        existing_order = orders.find_one({'_id': order_id})
        if not existing_order:
            return jsonify({'OK': False, 'error': 'Order not found'}), 404

        # Update the status of the order
        orders.update_one({'_id': order_id}, {'$set': {'status': new_status}})

        return jsonify({'OK': True, 'message': 'Order status updated successfully'}), 200

    except Exception as e:
        return jsonify({'OK': False, 'error': 'An unexpected error occurred'}), 500

# - Review all orders.
def review_all_orders():
    try:
        all_orders = list(orders.find({}))

        # Convert ObjectId instances to strings
        for order in all_orders:
            order['_id'] = str(order['_id'])
            order['dish_id'] = str(order['dish_id'])
            order['user_id'] = str(order['user_id'])
        return jsonify({'OK': True, 'orders': all_orders}), 200

    except Exception as e:
        return jsonify({'OK': False, 'error': 'An unexpected error occurred'}), 500