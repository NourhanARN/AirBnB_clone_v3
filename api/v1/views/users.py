#!/usr/bin/python3
"""this module for State objects that handles all
default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage
import json


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves the list of all users objects"""
    all_users = []
    users = storage.all(User).values()
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def user_by_id(user_id):
    """Retrieves a user object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """function that delete user object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """function that create user object"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'email' not in request_data:
        abort(400, 'Missing email')
    if 'password' not in request_data:
        abort(400, 'Missing password')
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """function that updates a user object"""
    user = storage.get(User, user_id)
    if user is None or user_id != user.id:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        ignored_keys = ["id", "email", "created_at", "updated_at"]
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
