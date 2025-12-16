# Added for MYSQL

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.services.user_service import create_user, get_user_by_email
from app.utils.response import success, error

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if get_user_by_email(data["email"]):
        return error("User already exists", 400)

    user = create_user(
        data["name"],
        data["email"],
        data["password"]
    )
    return success("User registered", {"id": user.id}, 201)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = get_user_by_email(data["email"])

    if not user or not user.check_password(data["password"]):
        return error("Invalid credentials", 401)

    token = create_access_token(identity=user.id)
    return success("Login successful", {"access_token": token})
