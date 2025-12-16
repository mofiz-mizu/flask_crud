# from flask import Blueprint, request
# from app.services.user_service import (
#     create_user, get_all_users, get_user,
#     update_user, delete_user
# )
# from app.schemas.user_schema import UserSchema
# from app.utils.response import success, error

# user_bp = Blueprint("users", __name__)
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

# @user_bp.route("/", methods=["POST"])
# def create():
#     data = request.get_json()
#     user = create_user(data["name"], data["email"])
#     return success("User created", user_schema.dump(user), 201)

# @user_bp.route("/", methods=["GET"])
# def list_users():
#     users = get_all_users()
#     return success("Users fetched", users_schema.dump(users))

# @user_bp.route("/<int:user_id>", methods=["GET"])
# def retrieve(user_id):
#     user = get_user(user_id)
#     if not user:
#         return error("User not found", 404)
#     return success("User fetched", user_schema.dump(user))

# @user_bp.route("/<int:user_id>", methods=["PUT"])
# def update(user_id):
#     user = get_user(user_id)
#     if not user:
#         return error("User not found", 404)

#     data = request.get_json()
#     updated = update_user(user, data["name"], data["email"])
#     return success("User updated", user_schema.dump(updated))

# @user_bp.route("/<int:user_id>", methods=["DELETE"])
# def delete(user_id):
#     user = get_user(user_id)
#     if not user:
#         return error("User not found", 404)

#     delete_user(user)
#     return success("User deleted")

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.user_service import (
    get_all_users, get_user, update_user, delete_user
)
from app.schemas.user_schema import UserSchema
from app.utils.response import success, error

user_bp = Blueprint("users", __name__)
schema = UserSchema()
schemas = UserSchema(many=True)

@user_bp.route("/", methods=["GET"])
@jwt_required()
def list_users():
    return success("Users fetched", schemas.dump(get_all_users()))

@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def retrieve(user_id):
    user = get_user(user_id)
    if not user:
        return error("User not found", 404)
    return success("User fetched", schema.dump(user))

@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update(user_id):
    user = get_user(user_id)
    if not user:
        return error("User not found", 404)

    data = request.get_json()
    update_user(user, data["name"], data["email"])
    return success("User updated", schema.dump(user))

@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete(user_id):
    user = get_user(user_id)
    if not user:
        return error("User not found", 404)

    delete_user(user)
    return success("User deleted")
