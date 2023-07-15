



# - Update the status of an order.
# - Review all orders.
# - Exit the system.

from flask import jsonify, request
from models.db import users, orders, menu
from bson.objectid import ObjectId
from pymongo import errors

# - Add a new dish to the menu.
def add_dish():
    try:
        dish = request.get_json()
        if not dish:
            return jsonify({'error': 'Invalid JSON data'}), 400
        menu.insert_one(dish)
        return jsonify({'message': 'Dish added successfully'}), 201
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

