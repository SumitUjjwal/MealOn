from flask import jsonify, request
from models.db import users, orders, menu
from bson.objectid import ObjectId
from pymongo import errors

# - Take a new order from a customer.
# Validate order_data
def validate_order_data(order_data):
    required_fields = ['dish_id', 'quantity']
    for order_item in order_data:
        for field in required_fields:
            if field not in order_item:
                return False
        if not isinstance(order_item['quantity'], int) or order_item['quantity'] <= 0:
            return False
    return True

# Function to place an order
def place_order():
    try:
        order_data = request.get_json()

        # Validate order_data
        if not isinstance(order_data, list) or not validate_order_data(order_data):
            return jsonify({'error': 'Invalid order data'}), 400

        in_stock_orders = []
        out_of_stock_orders = []

        for order_item in order_data:
            order_item['status'] = 'received'
            order_item['dish_id'] = ObjectId(order_item['dish_id'])
            order_item['user_id'] = ObjectId(request.user_id)  # Associate user_id with the order

            # Check if the item is in stock
            dish = menu.find_one({'_id': order_item['dish_id'], 'quantity': {'$gte': order_item['quantity']}})
            if dish:
                in_stock_orders.append(order_item)
            else:
                out_of_stock_orders.append(order_item)

        if in_stock_orders:
            if not out_of_stock_orders:
                # All items are in stock, place the orders directly
                orders.insert_many(in_stock_orders)
                return jsonify({'OK': True, 'message': 'Orders placed successfully', 'orders': in_stock_orders}), 201
            else:
                # Some items are out of stock, prompt the user to proceed with partial order
                message = f"Some items are out of stock: {out_of_stock_orders}. Do you want to proceed with the partial order for {in_stock_orders}? (yes/no)"
                return jsonify({'OK': False, 'error': message, 'in_stock_orders': [order_item for order_item in in_stock_orders], 'out_of_stock_orders': [order_item for order_item in out_of_stock_orders]}), 200

        return jsonify({'OK': False, 'error': 'Order quantity is greater than stock available for all items', 'out_of_stock_orders': [order_item for order_item in out_of_stock_orders]}), 400

    except errors.PyMongoError as e:
        return jsonify({'OK': False, 'error': str(e)}), 500
    except Exception as e:
        print('Error', e)
        return jsonify({'OK': False, 'error': 'An unexpected error occurred'}), 500
