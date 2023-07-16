# import pytest
import json
from flask import Flask, jsonify, request
from models.db import menu, users, orders
from app import app
from bson.objectid import ObjectId

# Test home route
def test_home():
    client = app.test_client()
    response = client.get('/')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['OK'] == True
    assert data['message'] == 'Welcome to MealOn!'

# ************************ ADMIN ROUTES ************************
# ************************ ADMIN ROUTES ************************
# ************************ ADMIN ROUTES ************************

# test get menu route
def test_get_menu():
    client = app.test_client()
    response = client.get('/admin/menu')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['OK'] == True

# test add dish route
def test_add_dish():
    client = app.test_client()
    headers = {'Content-Type': 'application/json'}
    data = {
        'title': 'Pizza',
        'price': 150,
        'quantity':10,
        'description': 'Delicious Italian Recipe made Pizza',
        'availability': 'true'
    }
    response = client.post('/admin/dish/add', headers=headers, json=data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['OK'] == True
    assert data['message'] == 'Dish added successfully'

# Test remove a dish route
def test_remove_dish():
    client = app.test_client()
    id = '64ad084ba62294d3541a855b'
    response = client.delete(f'admin/dish/remove/{id}')
    assert response.status_code == 200 or response.status_code == 404
    data = json.loads(response.data)
    assert data['message'].startswith('Dish with id:')

#Test update the availablity of the dish route
def test_update_availablity():
    client = app.test_client()
    id = '64ad084ba62294d3541a855b'
    qty = 10
    response = client.patch(f'admin/dish/update/{id}/{qty}')
    assert response.status_code == 200 or response.status_code == 404
    data = json.loads(response.data)
    assert data['message'].startswith('Dish with id:') 

#Test update the status of the order route
def test_update_order_status():
    client = app.test_client()
    headers = {'Content-Type': 'application/json'}
    data = {
        'orderid': '64b2ead84f930d7f0f6cec19',
        'status': 'accepted'
    }
    response = client.patch(f'admin/orders/status/update', headers = headers, json = data)
    assert response.status_code == 200 or response.status_code == 404
    data = json.loads(response.data)
    assert data['message'].startswith('Order status updated') or data['error'].startswith('Order not found')

#Test review all orders
def test_review_all_orders():
    client = app.test_client()
    response = client.get('/admin/orders')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['OK'] == True

# ************************ ADMIN ROUTES ************************
# ************************ ADMIN ROUTES ************************
# ************************ ADMIN ROUTES ************************