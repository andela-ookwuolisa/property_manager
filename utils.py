from flask import session, jsonify
from functools import wraps
from app import Base, db


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


class BaseClass:
    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name != "password_hash"
        }

    def save(self):
        try:
            db.add(self)
            db.commit()
        except Exception as e:
            err = str(e).split("[")[0].split(")")[-1]
            msg = f"{err.split(self.__tablename__)[0]}field {err.split(self.__tablename__)[-1]}"
            db.rollback()
            raise ValidationError(msg)

    def delete(self):
        try:
            db.delete(self)
            db.commit()
        except Exception as e:
            err = str(e).split("[")[0].split(")")[-1]
            msg = f"{err.split('users')[0]}field {err.split('users')[-1]}"
            db.rollback()
            raise ValidationError(msg)
