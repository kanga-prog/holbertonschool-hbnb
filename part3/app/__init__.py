from flask import Flask, Response, request
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import configurations
import os

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="development"):
    app = Flask(__name__)
    app.config.from_object(configurations.get(config_class))
    CORS(app, resources={r"/api/*": {
            "origins": "*",  # Autorise toutes les origines
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            response = Response()
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response

    @app.after_request
    def after_request(response):
        allowed_origins = ["http://127.0.0.1:8000", "http://localhost:8000"]
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    
    # Initialiser les extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    from app.api.v2.auth import api as auth_ns
    from app.api.v2.protected import api as protected_ns
    from app.api.v2.admins import api as admins_ns
    from app.api.v2.users import api as users_ns
    from app.api.v2.amenities import api as amenities_ns
    from app.api.v2.places import api as places_ns
    from app.api.v2.reviews import api as reviews_ns
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    # Charger la configuration appropriée selon l'environnement (développement ou production)
    # Création de l'API avec la documentation Swagger à l'endpoint /docs


    # save all the namespaces
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected') 

    if config_class == "development":
        api.add_namespace(admins_ns, path='/api/v1/admins')


    
    return app
