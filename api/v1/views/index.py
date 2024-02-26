#!/usr/bin/python3
"""create a route status on the object app_views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"users": User, "places": Place, "states": State,
           "cities": City, "amenities": Amenity, "reviews": Review}


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def count_stats():
    """retrieves the number of each objects by type"""
    result = {}
    for class_name, cls in classes.items():
        count = storage.count(cls)
        result[class_name] = count
    return jsonify(result)
