from flask import jsonify, request
from flask.blueprints import Blueprint

from flask_anime_api.studio.repository import StudioRepository
from flask_anime_api.model.schemas import StudioDTO, StudioCreateSchema

studio_bp = Blueprint('studios', __name__, url_prefix='/api/studios')

@studio_bp.get('/<studio_id>')
def get_by_id(studio_id):
    repo = StudioRepository()
    try:
        s = repo.get_by_id(studio_id)
    except ValueError:
        return f'No studio with id {studio_id}', 404
    
    return jsonify(s.model_dump())


@studio_bp.get('/')
def get_all():
    repo = StudioRepository()
    try:
        studios = repo.get_all()
    except:
        return 'Internal server error', 500
    
    return jsonify(
        [studio.model_dump() for studio in studios]
    )


@studio_bp.post('/')
def post_studio():
    ...