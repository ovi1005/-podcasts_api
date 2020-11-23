from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import os

# Init App
app = Flask(__name__)
dirB = os.path.abspath(os.path.dirname(__file__))
# Data Base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dirB, 'focus.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init Data Base
db = SQLAlchemy(app)


# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(20))

    def __init__(self, name, password):
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
        secondary=association_table,
        back_populates="podcasts")

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
    podcasts = db.relationship(
        "Podcast",
        secondary=association_table,
        back_populates="genres")

    def __init__(self, id_genre, name, url):
        self.id = id_genre
        self.name = name
        self.url = url


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
