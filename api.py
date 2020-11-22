from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Init App
app = Flask(__name__)
dirB = os.path.abspath(os.path.dirname(__file__))
# Data Base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dirB, 'focus.sqlite')
# Init Data Base
db = SQLAlchemy(app)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
