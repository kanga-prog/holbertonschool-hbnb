from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='privileges of admin or not')
})

user_update_model = api.model('User', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='privileges of admin or not')
})

@api.route('/')
class UserList(Resource):
    # POST /api/v1/users/ - Register a new user
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')    
    def post(self): 
        """Register a new user"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload
        # Simulate email uniqueness check   
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)            
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:  # Catch all other exceptions
            return {'message': str(e)}, 400

    # GET /api/v1/users/ - Retrieve a list of users
    @api.response(200, 'List of users retrieved successfully')
    @api.response(404, 'No users found')
    @api.response(400, 'Bad request')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_all_users()  # Ensure this method is defined in the facade
        if not users:
            return {'error': 'No users found'}, 404
        return [{'id': user.id, 
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'email': user.email,} for user in users], 200
        
@api.route('/<user_id>')
class UserResource(Resource):
    # GET /api/v1/users/<user_id> - Retrieve user details by ID
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
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
    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'You cannot change your email or pzssword')
    def put(self, user_id):
        """Update user details"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        user_data = api.payload

        if user_id != current_user and not claims.get('is_admin', False):
            return {'message': 'Unauthorized action'}, 403
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Check if the email or password are modified in the request
        email = user_data.get('email')
        password = user_data.get('password')

        # Prevent modification of the email or password for normal user
        if email and email != user.email and not claims.get('is_admin', False):
            return {'message': 'You cannot change your email or password'}, 400  # Return 400 if email is modified
        if password and password != user.password and not claims.get('is_admin', False):
            return {'message': 'You cannot change your email or password'}, 400  # Return 400 if password is modified
        
        try:    
            updated_user = facade.update_user(user_id, user_data)  # This is where the user is updated
            if not claims.get('is_admin', False):
                return {
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
            }, 200
            else:
                return {
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email' : updated_user.email
            }, 200 
        except Exception as e:  # Catch all other exceptions
            return {'message': str(e)}, 400

