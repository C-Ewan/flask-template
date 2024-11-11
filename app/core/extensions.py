from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager 
from flask_cors import CORS 


# Extension initialization 
db = SQLAlchemy()
migrate = Migrate() 
# jwt = JWTManager() 
cors = CORS() 

def init_extensions(app): 
    """ Initialize all extensions with the Flask application. """ 
    db.init_app(app) 
    migrate.init_app(app, db) 
    # jwt.init_app(app)
 