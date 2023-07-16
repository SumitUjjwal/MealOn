from flask import Blueprint
from controllers.userAuth import (login, signup)

# Create a new Blueprint instance
auth = Blueprint('auth', __name__)

# User login
@auth.route('/user/login', methods=['POST'])
def user_login_route():
    return login()

# User signup
@auth.route('/user/signup', methods=['POST'])
def user_signup_route():
    return signup()