from flask import Flask, jsonify, request

app = Flask(__name__)

anime = [
    {'id': 1, 'name': 'Cowboy Bebop'},
    {'id': 2, 'name': 'Lain'},
    {'id': 3, 'name': 'Eva'},
    {'id': 4, 'name': 'Frieren'},
    {'id': 5, 'name': 'Naruto'},
]


@app.get('/anime/<int:anime_id>')
def get_anime_by_id(anime_id):
    for a in anime:
        if a['id'] == anime_id:
            return jsonify(a)

        
@app.get('/anime')
def get_anime():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    return jsonify(
        {'meta': {'offset': offset, 'limit': limit}, 'data': anime}
    )

@app.post('/anime')
def post_anime():
    data = request.json
    anime.append({
        'id': len(anime) + 1,
        'name': data['name']
    })

    return jsonify({'status': 'OK'})