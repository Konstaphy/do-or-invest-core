from functools import wraps

import jwt
from flask import request

from src.exceptions.authorization_exception import AuthorizationException
from src.models.user import UserTokenData


def get_data_by_token():
    try:
        token = request.headers["authorization"].split(" ")[1]
    except KeyError:
        raise AuthorizationException()

    if token is None:
        raise AuthorizationException()

    try:
        data = jwt.decode(token, "secret", algorithms="HS256")
    except Exception as e:
        raise AuthorizationException()

    if data.get("id") is None:
        raise AuthorizationException()

    return data


def tokenized(func):
    @wraps(func)
    def wrapper():
        # get user data by token
        try:
            data = get_data_by_token()
        except AuthorizationException:
            return "Unauthorized", 401
        return func(UserTokenData(data.get("id"), data.get("username")))

    return wrapper
