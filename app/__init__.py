import os
from flask import Flask, send_from_directory
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')


    CORS(app)

    @app.route('/')
    def index():
        return "Welcome to the Pet Shelter API!"

    @app.route('/translations/<language_code>.json')
    def serve_translations(language_code):
        # Get the absolute path of the 'translates' directory
        translates_dir = os.path.abspath('translates')
        # Serve the file from that directory
        return send_from_directory(translates_dir, f'{language_code}.json')

    from .routes.shelter import shelter_routes

    app.register_blueprint(shelter_routes, url_prefix='/shelter')

    return app
