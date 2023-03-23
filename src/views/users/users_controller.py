import datetime
import uuid

from flask import Blueprint, Request, Response, request, jsonify
import jwt
from flask_cors import cross_origin

from src.models.user import User

users = Blueprint("users", __name__, url_prefix="/users")


# на регистрацию создаем токен и сохраняем в локал сторейдже, сохраняем пользователя
# на логин проверяем пользователя и пароль создаем токен и сохраняем в локал сторейдже
# рефреш - проверяем текущий токен и пересоздаем

@users.route("/login")
@cross_origin(supports_credentials=True)
def login():
    authorization = request.authorization
    if not authorization:
        return "Unauthorized", 401
    user = User.get_or_none(User.name == authorization.get("username"))
    if user.password == authorization.get("password"):
        jwt_token = jwt.encode(
            {"name": user.name, "id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
            key='secret',
            algorithm="HS256")
        return jsonify({"id": user.id, "access_token": jwt_token})
    return "Unauthorized", 401


@users.route("/refresh")
@cross_origin(supports_credentials=True)
def refresh():
    # Token like "Bearer {token}"
    authorization = request.headers.get("authorization")
    token = authorization.split(" ")[1]
    if not token:
        return "Unauthorized", 401
    try:
        data = jwt.decode(token, "secret", algorithms="HS256")
    except jwt.exceptions.ExpiredSignatureError:
        return "Unauthorized", 401

    if datetime.datetime.fromtimestamp(data.get("exp")) < datetime.datetime.utcnow():
        return "Unauthorized", 401
    return jwt.encode({"name": data.get("name"), "id": data.get("id"),
                       "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, "secret", algorithm="HS256")


@users.route("/sign-up", methods=["POST"])
@cross_origin(supports_credentials=True)
def sign_up():
    # username and password
    authorization = request.authorization
    # email
    request_body = request.get_json(force=True)
    User(name=authorization.get("username"), password=authorization.get("password"),
         email=request_body.get("email")).save()

    all_users = [user for user in User.select().dicts()]
    return jsonify(all_users)
