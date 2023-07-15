# import pytest
import json
from app import app

def test_home():
    client = app.test_client()
    response = client.get('/')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['OK'] == True
    assert data['message'] == 'Welcome to MealOn!'
