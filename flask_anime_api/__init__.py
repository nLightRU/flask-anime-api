from flask import Flask

from flask_anime_api.model.database import db
from flask_anime_api.anime.routes import anime_bp

from flask_anime_api.config import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(anime_bp)

    return app