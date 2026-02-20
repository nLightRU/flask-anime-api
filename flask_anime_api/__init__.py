from flask import Flask, json
from werkzeug.exceptions import BadRequest, NotFound

from flask_anime_api.model.database import db
from flask_anime_api.anime.routes import anime_bp
from flask_anime_api.studio.routes import studio_bp
from flask_anime_api.user.routes import users_bp
from flask_anime_api.config import Config


def handle_4xx(e):
    response = e.get_response()
    response.data = json.dumps({
    "code": e.code,
    "name": e.name,
    "description": e.description,
    })
    response.content_type = "application/json"
    return response


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    app.json.sort_keys = False 
    app.register_error_handler(BadRequest, handle_4xx)
    app.register_error_handler(NotFound, handle_4xx)
    
    db.init_app(app)

    app.register_blueprint(anime_bp)
    app.register_blueprint(studio_bp)
    app.register_blueprint(users_bp)

    return app