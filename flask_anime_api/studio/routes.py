from flask import jsonify, request
from flask.blueprints import Blueprint
from pydantic import ValidationError

from flask_anime_api.studio.service import StudioService
from flask_anime_api.model.schemas import BaseStudio, StudioResponseSchema

studio_bp = Blueprint('studios', __name__, url_prefix='/api/studios')

@studio_bp.get('/<studio_id>')
def get_by_id(studio_id):
    service = StudioService()
    try:
        studio = service.get_by_id(studio_id)
    except ValueError:
        return f'No studio with id {studio_id}', 404
    
    if not studio:
        return f'No studio with id {studio_id}', 404

    studio_response = StudioResponseSchema(**studio.model_dump())

    return jsonify(studio_response.model_dump())


@studio_bp.get('/')
def get_all():
    service = StudioService()
    try:
        studios = service.get_all()
    except:
        return 'Internal server error', 500
    
    resp_data = [StudioResponseSchema(**s.model_dump()) for s in studios]

    return jsonify([studio.model_dump() for studio in resp_data])


@studio_bp.post('/')
def post_studio():
    try: 
        json = request.get_json()
        studio_data = BaseStudio(**json)
    except ValidationError:
        return 'Missing requred fields', 400
        
    service = StudioService()
    try:
        studio = service.create(studio_data)
    except:
        raise

    return jsonify(studio.model_dump())


@studio_bp.put('/<studio_id>')
def put_studio(studio_id):
    try:
        json = request.get_json()
        studio = BaseStudio(**json)
    except ValidationError:
        return 'Missing requred fields', 400

    service = StudioService()

    try:
        studio = service.update(studio_id, studio)
    except ValueError:
        return f'Studio with id {studio_id} not found', 404
    

    return jsonify(studio.model_dump())


@studio_bp.delete('/<studio_id>')
def delete_studio(studio_id):
    service = StudioService()

    try:
        service.delete(studio_id)
    except ValueError:
        return f'Studio with id {studio_id} not found', 404
    
    return jsonify({'status': 'No Content'}), 204