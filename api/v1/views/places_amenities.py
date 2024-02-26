#!/usr/bin/python3
"""this module for place-amenities objects that handles all
default RESTFul API actions"""
from flask import jsonify, abort, make_response
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_amenities = []
    if getenv('HBNB_TYPE_STORAGE') == "db":
        for amenity in place.amenities:
            all_amenities.append(amenity.to_dict())
    else:
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            all_amenities.append(amenity.to_dict())          
    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_Amenity_by_id(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity_id != place.amenity_id:
            abort(404)       
        storage.delete(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.delete(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_Amenity_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity_id == place.amenity_id:  
            return jsonify(amenity.to_dict()), 200
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
