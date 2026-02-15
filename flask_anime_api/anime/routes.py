from uuid import UUID
from flask import Blueprint, request, jsonify, abort

from flask_anime_api.anime.service import AnimeService
from flask_anime_api.anime.repository import AnimeRepository
from flask_anime_api.model.schemas import AnimeCreateUpdateScheme, AnimeDTO, AnimeResponseScheme

anime_bp = Blueprint('anime', __name__, url_prefix='/api/anime')

@anime_bp.get('/<anime_id>')
def get_anime_by_id(anime_id) -> AnimeResponseScheme:
    s = AnimeService()
    
    try:
        a = s.get_by_id(UUID(anime_id))
    except ValueError:
        return f'Anime with id {anime_id} not found', 404

    data = {
        'id': a.id,
        'title': a.title,
        'episodes': a.episodes,
        'studios': [{'id': s.id, 'name': s.name} for s in a.studios]
    }

    return jsonify(data)

        
@anime_bp.get('/')
def get_anime_all() -> list[AnimeResponseScheme]:
    offset=request.args.get('offset')
    limit=request.args.get('limit')
    s = AnimeService()
    anime = s.get_all()
    
    data = {
        'meta (IN DEVELOPMENT)': {
            'offset': offset,
            'limit': limit, 
            'count': 'IN DEVELOPMENT'
        },
        'data': [ a.model_dump() for a in anime ]
    }

    return jsonify(data)


@anime_bp.post('/')
def post_anime():
    try:
        json = request.get_json()
        data = AnimeCreateUpdateScheme(**json)
    except Exception:
        return 'Missing requred fields', 400    

    repo = AnimeRepository()
    new_anime = repo.create(data)

    if not new_anime:
        abort(500)


    return jsonify(new_anime.model_dump())


@anime_bp.put('/<anime_id>')
def put_anime(anime_id):
    try:
        json = request.get_json()
        new_data = AnimeCreateUpdateScheme(**json)
    except:
        return 'Missing requred fields', 400
    
    repo = AnimeRepository()
    try:
        a = repo.update(anime_id, new_data)
    except ValueError:
        return f'Anime with id {anime_id} not found', 404
    
    return jsonify(**a.model_dump())


@anime_bp.delete('/<anime_id>')
def delete_anime(anime_id):
    repo = AnimeRepository()
    try:
        repo.delete(anime_id)
    except ValueError:
        return f'Anime with id {anime_id} not found', 404
    
    return jsonify({'status': 'No Content'}), 204
