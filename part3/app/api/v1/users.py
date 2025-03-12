from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_bcrypt import Bcrypt
from app.models import user


api = Namespace('users', description='User operations')

from flask_bcrypt import Bcrypt
from app.models.user import User  # Assurez-vous d'importer le modèle User
from app import facade  # Assurez-vous d'importer votre facade correctement

@api.route('/')
class UserList(Resource):
    # POST /api/v1/users/ - Register a new user
    @api.expect(user, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self): 
        """Register a new user"""
        
        user_data = api.payload
        
        # Vérification si l'email est déjà pris
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        # Création d'un nouvel objet User
        try:
            new_user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password'],
                place_list=user_data.get('place_list', []),
                reviews_posted=user_data.get('reviews_posted', []),
                is_admin=user_data.get('is_admin', False)
            )
            
            # Hachage du mot de passe avant de sauvegarder
            new_user.hash_password(new_user.password)
            
            # Sauvegarde de l'utilisateur (assurez-vous que votre façade a cette méthode)
            facade.save_user(new_user)

            # Réponse sans le mot de passe
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'place_list': new_user.place_list
            }, 201

        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:  # Capture toutes les autres exceptions
            return {'message': str(e)}, 400


    # GET /api/v1/users/ - Retrieve a list of users
    @jwt_required()  # Protect this endpoint with JWT
    @api.response(200, 'List of users retrieved successfully')
    @api.response(404, 'No users found')
    @api.response(400, 'Bad request')
    def get(self):
        """Retrieve a list of users"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the JWT
        # Optional: Use current_user to verify if the user has the right to view the data
        users = facade.get_all_users()  # Ensure this method is defined in the facade
        if not users:
            return {'error': 'No users found'}, 404
        return [{'id': user.id, 
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'email': user.email,
                'place_list': user.place_list,
                'reviews_posted': user.reviews_posted} for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    # GET /api/v1/users/<user_id> - Retrieve user details by ID
    @jwt_required()  # Protect this endpoint with JWT
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the JWT
        # Optional: Check if the user has the right to access this resource
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'email': user.email,
                'place_list': user.place_list,
                'reviews_posted': user.reviews_posted}, 200

    # PUT /api/v1/users/<user_id> - Update user details
    @jwt_required()  # Protect this endpoint with JWT
    @api.expect(user, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the JWT
        # Optional: Check if the user is allowed to update the user data
        user_data = api.payload
        try:    
            updated_user = facade.update_user(user_id, user_data)  # This is where the user is updated
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'place_list': updated_user.place_list
            }, 200
        except Exception as e:  # Catch all other exceptions
            return {'message': str(e)}, 400
