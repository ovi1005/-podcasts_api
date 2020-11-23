from api import db
from api import Genre
from api import Podcast
import requests

# Create all data base schema
print('Creating schema ...')
db.create_all()

# Import data json
data = requests.get('https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/100/explicit.json')
print('Inserting genres ...')
for podcast in data.json()['feed']['results']:
    for genre in podcast['genres']:
        genre_exist = Genre.query.filter_by(id=genre['genreId']).first()
        if genre_exist is None:
            new_genre = Genre(id_genre=genre['genreId'], name=genre['name'], url=genre['url'])
            db.session.add(new_genre)
            db.session.commit()

print('Inserting podcast ...')
for podcast in data.json()['feed']['results']:
    podcast_exist = Podcast.query.filter_by(id=podcast['id']).first()
    if podcast_exist is None:
        id_pod = podcast['id']
        artist_name = podcast['artistName']
        release_date = podcast['releaseDate']
        name = podcast['name']
        kind = podcast['kind']
        try:
            copyright_pod = podcast['copyright']
        except:
            copyright_pod = None
        try:
            artist_id = podcast['artistId']
        except:
            artist_id = None
        try:
            content_advisory_rating = podcast['contentAdvisoryRating']
        except:
            content_advisory_rating = None
        try:
            artist_url = podcast['artistUrl']
        except:
            artist_url = None
        artwork_url100 = podcast['artworkUrl100']
        url = podcast['url']
        new_podcast = Podcast(id_pod=id_pod, artist_name=artist_name, release_date=release_date,
                              name=name, kind=kind, copyright_pod=copyright_pod,
                              artist_id=artist_id, content_advisory_rating=content_advisory_rating,
                              artist_url=artist_url, artwork_url100=artwork_url100, url=url)
        for genre in podcast['genres']:
            genre_data = Genre.query.filter_by(id=genre['genreId']).first()
            new_podcast.genres.append(genre_data)
        db.session.add(new_podcast)
        db.session.commit()

print('Database and completed data')
