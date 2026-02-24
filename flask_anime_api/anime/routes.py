"""
Модуль содержит в себе функции обработчики роутов, связанных с Anime
* GET /api/anime/
* GET /api/anime/{id}
* POST /api/anime/
* PUT /api/anime/{id}
* DELETE /api/anime/{id}
"""

from uuid import UUID

from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import BadRequest, NotFound
from pydantic import ValidationError

from flask_anime_api.anime.service import AnimeService
from flask_anime_api.anime.repository import AnimeRepository
from flask_anime_api.model.schemas import AnimeUpdateScheme, AnimeResponseScheme, AnimeCreateScheme

anime_bp = Blueprint('anime', __name__, url_prefix='/api/anime')


@anime_bp.get('/<anime_id>')
def get_anime_by_id(anime_id) -> AnimeResponseScheme:
    """
    Функция обработчик метода GET /api/anime/{id}
    Возвращает JSON объект сущности Anime
    """
    s = AnimeService()
    a = s.get_by_id(UUID(anime_id))

    if not a:
        raise NotFound(f'Anime with id {anime_id} not found')

    return a.model_dump(mode='json')


@anime_bp.get('/')
def get_anime_all() -> list[AnimeResponseScheme]:
    """
    Функция обработчик метода GET /api/anime/{id}
    Возвращает JSON список сущностей Anime
    """
    offset=request.args.get('offset')
    limit=request.args.get('limit')
    s = AnimeService()
    anime = s.get_all()

    # Getting right order of fields
    data = {
        'meta (IN DEVELOPMENT)': {
            'offset': offset,
            'limit': limit, 
            'count': 'IN DEVELOPMENT'
        },
        'data': [a.model_dump(mode='json') for a in anime]
    }

    return jsonify(data)


@anime_bp.post('/')
def post_anime():
    """
    Функция обработчик метода POST /api/anime
    Возвращает JSON объект сущности Anime
    """
    try:
        json = request.get_json()
        data = AnimeCreateScheme(**json)
    except ValidationError as e:
        msg = e.errors()[0]['msg']
        loc = list(e.errors()[0]['loc'])
        return BadRequest(f"{msg} {loc}")

    try:
        s = AnimeService()
        a = s.create_anime(data)
    except:
        abort(500)

    return a.model_dump(mode='json')


@anime_bp.put('/<anime_id>')
def put_anime(anime_id):
    """
    Функция обработчик метода PUT /api/anime/{id}
    Возвращает JSON объект сущности Anime с изменёнными полями
    """
    try:
        json = request.get_json()
        anime_data = AnimeUpdateScheme(**json)
    except ValidationError as e:
        msg = e.errors()[0]['msg']
        loc = list(e.errors()[0]['loc'])
        return BadRequest(f"{msg} {loc}")

    s = AnimeService()
    a = s.update_anime(anime_id, anime_data)
    if not a:
        return NotFound(f'Anime with id {anime_id} not found')

    return a.model_dump(mode='json')


@anime_bp.delete('/<anime_id>')
def delete_anime(anime_id):
    """
    Функция-обработчик роута DELETE /api/anime/{id}
    Реализует мягкое удаление в таблице anime
    В таблице anime_studios записи удаляются
    """
    repo = AnimeRepository()
    deleted = repo.delete(anime_id)

    if not deleted:
        return NotFound(f'Anime with id {anime_id} not found')

    return jsonify({'code': 204, 'status': 'No Content'}), 204
