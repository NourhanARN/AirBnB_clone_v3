#!/usr/bin/python3
"""this module for Amenity objects that handles all
default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all amenities objects"""
    all_amenities = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_by_id(amenity_id):
    """Retrieves Amenity object by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """function that delete amenity object by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """function that create amenity object"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    new_amenity = Amenity(name=request_data['name'])
    storage.new(new_amenity)
    storage.save()
    new_amenity_dict = new_amenity.to_dict()
    return jsonify(new_amenity_dict), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_Amenity(amenity_id):
    """function that updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        ignored_keys = ["id", "created_at", "updated_at"]
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    new_amenity_dict = amenity.to_dict()
    return jsonify(new_amenity_dict), 200
