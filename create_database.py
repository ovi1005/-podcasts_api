from api import db
import requests

# Create all data base schema
db.create_all()

# Import data json
data = requests.get('https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/100/explicit.json')
#for podcast in data.json()['feed']['results']:
    #print(len(podcast))
