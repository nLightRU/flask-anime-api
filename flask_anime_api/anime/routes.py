from uuid import UUID
from flask import Blueprint, request, jsonify, abort

from flask_anime_api.anime.repository import AnimeRepository
from flask_anime_api.model.schemas import AnimeCreateScheme, AnimeDTO

anime_bp = Blueprint('anime', __name__, url_prefix='/api/anime')

@anime_bp.get('/<anime_id>')
def get_anime_by_id(anime_id):
    repo = AnimeRepository()
    
    try:
        a = repo.get_by_id(anime_id)
    except ValueError:
        return f'Anime with id {anime_id} not found', 404

    return jsonify(a.model_dump())

        
@anime_bp.get('/')
def get_anime():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    repo = AnimeRepository()
    anime = repo.get_all()
    return jsonify([a.model_dump() for a in anime])


@anime_bp.post('/')
def post_anime():
    try:
        json = request.get_json()
        data = AnimeCreateScheme(**json)
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
        new_data = AnimeDTO(**json)
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
