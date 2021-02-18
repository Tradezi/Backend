
import json
from flask import Blueprint, request, Response, make_response, jsonify

# from app.user.controller import user_login, create_new_user, change_password

user = Blueprint('user', __name__)

@user.route("/login", methods=["GET"])
def user_login():
    return "User, Logged in!"