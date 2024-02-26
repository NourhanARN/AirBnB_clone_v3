#!/usr/bin/python3
"""app"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(self):
    ''' closes storage engine '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    ''' handles 404 error and gives json formatted response '''
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
# #!/usr/bin/python3
# """this module configures and runs the Flask application"""
# from flask import Flask, jsonify, make_response
# from models import storage
# from api.v1.views import app_views
# import os
# from flask import jsonify
# from flask_cors import CORS


# app = Flask(__name__)
# # CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
# app.register_blueprint(app_views)


# @app.teardown_appcontext
# def close_storage(exception):
#     """closes the storage on teardown"""
#     storage.close()


# @app.errorhandler(404)
# def handle_not_found_error(e):
#     """handle 404 error"""
#     return make_response(jsonify({'error': 'Not found'}), 404)


# if __name__ == "__main__":
#     host = os.getenv('HBNB_API_HOST', '0.0.0.0')
#     port = int(os.getenv('HBNB_API_PORT', 5000))
#     app.run(host=host, port=port, threaded=True)
