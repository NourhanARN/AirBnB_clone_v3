#!/usr/bin/python3
"""this module for State objects that handles all
default RESTFul API actions"""
from flask import jsonify, abort, request , make_response
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def all_cities_state(state_id):
    """Retrieves the list of all City objects of a State"""
    all_cities = []  
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = storage.all(City)
    for key, value in cities.items():
        if state_id == value.state_id:
            all_cities.append(value.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_by_id(city_id):
    """Retrieves a city object by its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    """function that delete city object by its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """function that create city object"""
    request_data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    new_city = City(**request_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """function that updates a city object"""
    if not request.is_json:
       return make_response("Not a JSON", 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_data = request.get_json()
    for key, value in request_data.items():
        ignored_keys = ["id", "state_id", "created_at", "updated_at"]
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
