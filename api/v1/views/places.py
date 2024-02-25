#!/usr/bin/python3
"""this module for State objects that handles all
default RESTFul API actions"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_cities_place(city_id):
    """Retrieves the list of all Place objects of a City"""
    all_places = []
    places = storage.all(Place)
    for key, value in places.items():
        if city_id == value.city_id:
            all_places.append(value.to_dict())
    if not all_places:
        abort(404)
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def place_by_id(place_id):
    """Retrieves a place object by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_by_id(place_id):
    """function that delete place object by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """function that create place object"""
    if not request.is_json:
        return make_response("Not a JSON", 400)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_data = request.get_json()
    if 'name' not in request_data:
        abort(400, 'Missing name')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    user_id = request_data.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)    
    new_place = Place(**request_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """function that updates a place object"""
    if not request.is_json:
        return make_response("Not a JSON", 400)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    for key, value in request_data.items():
        ignored_keys = ["id", "city_id", "user_id", "created_at", "updated_at"]
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
