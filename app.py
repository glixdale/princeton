from flask import Flask
from flask_cors import CORS, cross_origin
from Blueprints.property import bp as property_bp
from database import db, seed
from Models.Property import Property

def create_app():
    # # create the extension
    # db = SQLAlchemy()
    # # create the app
    app = Flask(__name__)
    app.app_context().push()
    # configure the SQLite database, relative to the app instance folder
    # \/ Move this to .env
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
    app.json.sort_keys = False
    #Specify for localhost and Prod site
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # initialize the app with the extension
    # from Models import *
    # migrate = Migrate(app,db)

    db.init_app(app)
    app.register_blueprint(property_bp)

    return app

if __name__=="__main__":
    
    app = create_app()
        # Set the number of properties you want to generate and seed
    num_properties_to_seed = 100

    # Create tables if they do not exist
    with app.app_context():
        db.create_all()

    # Seed the database with random properties
    if Property.query.first() is None:
        seed.seed_database(num_properties_to_seed)
    app.run(host='0.0.0.0',port=8000,debug=True)