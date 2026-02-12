from flask import Blueprint, request, jsonify

from .data import anime_data

anime_bp = Blueprint('anime', __name__, url_prefix='/api/anime')

@anime_bp.get('/<int:anime_id>')
def get_anime_by_id(anime_id):
    for a in anime_data:
        if a['id'] == anime_id:
            return jsonify(a)

        
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