from datetime import datetime
from flask import request


def add_updated_at_to_request_data():
    request.json['updatedAt'] = datetime.now()

