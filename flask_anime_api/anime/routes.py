from uuid import UUID
from flask import Blueprint, request, jsonify, abort

from flask_anime_api.anime.repository import AnimeRepository
from flask_anime_api.model.schemas import AnimeCreateScheme

anime_bp = Blueprint('anime', __name__, url_prefix='/api/anime')

@anime_bp.get('/<anime_id>')
def get_anime_by_id(anime_id):
    repo = AnimeRepository()
    
    a = repo.get_by_id(anime_id)
    
    if not a: 
        abort(404)

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

    return jsonify({'anime': new_anime.model_dump()})

