#!/usr/bin/python3
"""this module for State objects that handles all
default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


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


# @app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
# def create_city(state_id):
#     """function that create city object"""
#     request_data = request.get_json()
#     if not request_data:
#         abort(400, 'Not a JSON')
#     if 'name' not in request_data:
#         abort(400, 'Missing name')
#     name = request_data.get('name')
#     new_city = City(state_id=state_id, name=name)
#     storage.new(new_city)
#     storage.save()
#     new_city_dict = new_city.to_dict()
#     return jsonify(new_city_dict), 201


# @app_views.route('/cities/<city_id>', methods=['PUT'])
# def update_city(city_id):
#     """function that updates a city object"""
#     city = storage.get(City, city_id)
#     if city is None:
#         abort(404)
#     request_data = request.get_json()
#     if not request_data:
#         abort(400, 'Not a JSON')
#     for key, value in request_data.items():
#         ignored_keys = ["id", "state_id", "created_at", "updated_at"]
#         if key not in ignored_keys:
#             setattr(city, key, value)
#     storage.save()
#     new_city_dict = city.to_dict()
#     return jsonify(new_city_dict), 200
