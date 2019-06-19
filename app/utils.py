from flask import session, jsonify
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            session["username"]
            return f(*args, **kwargs)
        except KeyError:
            return jsonify({"message": "This route requires login"}), 401

    return decorated


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


