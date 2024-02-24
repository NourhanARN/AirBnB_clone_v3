#!/usr/bin/python3
"""this module for State objects that handles all
default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    all_states = []
    """Retrieves the list of all State objects"""
    states = storage.all(City).values()
    for state in states:
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_by_id(state_id):
    """Retrieves the list of State object by its id"""
    state = storage.get(City, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    """function that delete State object by its id"""
    state = storage.get(City, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """function that create state object"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    new_state = City(name=request_data['name'])
    storage.new(new_state)
    storage.save()
    new_state_dict = new_state.to_dict()
    return jsonify(new_state_dict), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """function that updates a State object"""
    state = storage.get(City, state_id)
    if state is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        ignored_keys = ["id", "created_at", "updated_at"]
        if key not in ignored_keys:
            setattr(state, key, value)
    storage.save()
    new_state_dict = state.to_dict()
    return jsonify(new_state_dict), 200
