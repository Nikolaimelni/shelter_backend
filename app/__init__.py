from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')


    CORS(app)

    from .routes.shelter import shelter_routes

    app.register_blueprint(shelter_routes, url_prefix='/shelter')

    return app
