from flask import Blueprint
from controllers.userAuth import (login, signup)

# Create a new Blueprint instance
auth = Blueprint('auth', __name__)

@auth.route('/user/login', methods=['POST'])
def user_login_route():
    return login()

@auth.route('/user/signup', methods=['POST'])
def user_signup_route():
    return signup()