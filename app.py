from flask import Flask, jsonify, request
from models.db import menu, orders
from routes.adminRouter import admin
from routes.authRouter import auth
from routes.userRouter import user
from middleware.createdAt import add_created_at_to_request_data
from middleware.updatedAt import add_updated_at_to_request_data

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'OK': True, 'message': 'Welcome to MealOn!'}), 200

@app.before_request
def before_request():
    if request.method == 'POST' or request.method == 'PUT':
        route = request.url_rule
        if not str(route).startswith('/auth'):
            add_created_at_to_request_data()
    elif request.method == 'PATCH':
        add_updated_at_to_request_data()

# @app.route('/delete_documents', methods=['DELETE'])
# def delete_documents():
#     try:
#         orders.delete_many({})
#         return jsonify({'message': 'Deleted all documents from orders'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)