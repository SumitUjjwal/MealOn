from datetime import datetime
from flask import request


def add_created_at_to_request_data():
    request.json['createdAt'] = datetime.now()

