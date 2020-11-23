from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
import json
import os
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps

# Init App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'focus_secret'
dirB = os.path.abspath(os.path.dirname(__file__))
# Data Base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dirB, 'focus.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init Data Base
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(20))

    def __init__(self, public_id, name, password):
        self.public_id = public_id
        self.name = name
        self.password = password


# GenrePodcasts
association_table = db.Table('genre_podcasts',
                             db.Column('podcast_id', db.Integer, db.ForeignKey('podcast.id')),
                             db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
                             )


# Podcast Class/Model
class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(100))
    release_date = db.Column(db.String(10))
    name = db.Column(db.String(100))
    kind = db.Column(db.String(100))
    copyright_pod = db.Column(db.String(600), nullable=True)
    artist_id = db.Column(db.Integer, nullable=True)
    content_advisory_rating = db.Column(db.String(100), nullable=True)
    artist_url = db.Column(db.String(100), nullable=True)
    artwork_url100 = db.Column(db.String(100))
    url = db.Column(db.String(100))
    genres = db.relationship(
        "Genre",
        secondary=association_table)

    def __init__(self, id_pod, artist_name, release_date, name,
                 kind, copyright_pod, artist_id, content_advisory_rating,
                 artist_url, artwork_url100, url):
        self.id = id_pod
        self.artist_name = artist_name
        self.release_date = release_date
        self.name = name
        self.kind = kind
        self.copyright_pod = copyright_pod
        self.artist_id = artist_id
        self.content_advisory_rating = content_advisory_rating
        self.artist_url = artist_url
        self.artwork_url100 = artwork_url100
        self.url = url


# Genre Class/Model
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(100))

    def __init__(self, id_genre, name, url):
        self.id = id_genre
        self.name = name
        self.url = url


# Genre Schema
class GenreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'url')


# Init Genre schema
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


# Podcast Schema
class PodcastSchema(ma.Schema):
    genres = fields.Nested(GenreSchema, many=True)

    class Meta:
        fields = ('id', 'artist_name', 'release_date', 'name',
                  'kind', 'copyright_pod', 'artist_id', 'content_advisory_rating',
                  'artist_url', 'artwork_url100', 'url', 'genres')


# Init Podcast schema
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)


# Token required
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id' : user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# Podcasts search
@app.route('/podcast/<value>', methods=['GET'])
@token_required
def get_podcast(current_user, value):
    podcasts = Podcast.query.filter(Podcast.name.ilike("%" + value + "%")).all()
    result = podcasts_schema.dump(podcasts)
    return jsonify(result)


# Save the top 20 podcasts
@app.route('/podcast/top20', methods=['GET'])
@token_required
def get_top_podcast(current_user):
    podcasts = Podcast.query.limit(20)
    result = podcasts_schema.dump(podcasts)
    with open(os.path.join(dirB, 'podcasts_separate_data.json'), 'w') as file:
        json.dump(result, file)
    return jsonify(result)


# Replace the top 20 podcasts for bottom 20
@app.route('/podcast/bottom20', methods=['GET'])
@token_required
def get_bottom_podcast(current_user):
    podcasts = Podcast.query.order_by(Podcast.id.desc()).limit(20)
    result = podcasts_schema.dump(podcasts)
    with open(os.path.join(dirB, 'podcasts_separate_data.json'), 'w') as file:
        json.dump(result, file)
    return jsonify(result)


@app.route('/podcast/<id>', methods=['DELETE'])
@token_required
def delete_podcast(current_user, id):
    podcast = Podcast.query.get(id)
    if podcast is None:
        return jsonify({'message': 'Podcast not found, could not be deleted'})
    else:
        db.session.delete(podcast)
        db.session.commit()
        return jsonify({'message': 'Successfully deleted from the podcast with id: ' +
                                   str(podcast.id) + ' and name: ' + podcast.name})


# Podcasts group_by_genre
@app.route('/podcast/group_by_genre', methods=['GET'])
@token_required
def get_podcast_group_by_genre(current_user):
    slq_query = "SELECT p.name as 'name_p', p.artist_name, g.name as 'name_g', g.id" \
                " FROM genre_podcasts as 'gp',podcast as 'p', genre as 'g' " \
                "WHERE gp.genre_id = g.id AND gp.podcast_id = p.id " \
                "ORDER BY gp.genre_id"
    podcasts = db.engine.execute(slq_query)
    out_podcast = []
    out_genre = {}
    flag = None
    for podcast in podcasts:
        podcast_data = {}
        podcast_data['name_podcast'] = podcast.name_p
        podcast_data['artist_name'] = podcast.artist_name
        if flag is not None:
            if flag != podcast.name_g:
                out_genre.update({flag: out_podcast})
                out_podcast = []
        flag = podcast.name_g
        out_podcast.append(podcast_data)
    out_genre.update({flag: out_podcast})
    return jsonify(out_genre)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
