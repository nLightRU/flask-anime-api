from flask import Flask

from .anime_routes import anime_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(anime_bp)

    return app