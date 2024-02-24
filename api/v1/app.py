#!/usr/bin/python3
"""this module configures and runs the Flask application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def handle_not_found_error(e):
    """handle 404 error"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response
    


if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST") is None:
        host = "0.0.0.0"
    else:
        host = os.getenv("HBNB_API_HOST")
    if os.getenv("HBNB_API_PORT") is None:
        port = 5000
    else:
        port = int(os.getenv("HBNB_API_PORT"))
    app.run(host=host, port=port, threaded=True)
