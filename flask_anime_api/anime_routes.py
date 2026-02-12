from flask import Blueprint, request, jsonify, abort

from .anime_repository import AnimeRepository
from .data import anime_data

anime_bp = Blueprint('anime', __name__, url_prefix='/api/anime')

@anime_bp.get('/<int:anime_id>')
def get_anime_by_id(anime_id):
    repo = AnimeRepository(repo_data=anime_data)
    
    a = repo.get_by_id(anime_id)
    
    if not a: 
        abort(404)

    return jsonify(a.model_dump())

        
@anime_bp.get('/')
def get_anime():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    return jsonify(
        {'meta': {'offset': offset, 'limit': limit}, 'data': anime_data}
    )


@anime_bp.post('/')
def post_anime():
    data = request.json
    anime_data.append({
        'id': len(anime_data) + 1,
        'name': data['name']
    })

    return jsonify({'status': 'OK'})