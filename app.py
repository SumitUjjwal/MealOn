from flask import Flask, jsonify
from routes.adminRouter import admin
from routes.authRouter import auth
from routes.userRouter import user


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'OK': True, 'message': 'Welcome to MealOn!'}), 200

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)