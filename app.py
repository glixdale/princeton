from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.app_context().push()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
app.json.sort_keys = False
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# initialize the app with the extension
# from Models import *
# migrate = Migrate(app,db)

db.init_app(app)