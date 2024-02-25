#!/usr/bin/python3
"""this module for State objects that handles all
default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def all_reviews_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    all_reviews = []
    reviews = storage.all(Review)
    for key, value in reviews.items():
        if place_id == value.place_id:
            all_reviews.append(value.to_dict())
    if not all_reviews:
        abort(404)
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_by_id(review_id):
    """Retrieves a review object by its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_by_id(review_id):
    """function that delete review object by its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """function that create place object"""
    request_data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    user_id = request_data.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'text' not in request_data:
        abort(400, 'Missing text')   
    new_review = Place(**request_data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """function that updates a place object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
