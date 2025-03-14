# app/api/v2/admins.py
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('admins', description='Opérations pour gérer les administrateurs')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='privileges of admin or not')
})

user_upadate_model = api.model('User', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='privileges of admin or not')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=True, description='Description of the amenity')
})

amenity_upadate_model = api.model('Amenity', {
    'name': fields.String(required=False, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity')
})

@api.route('/users')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403


        user_data = api.payload
        email = user_data.get('email')

        # email uniqueness check 
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email, 'place_list': new_user.place_list}, 201
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @api.expect(user_upadate_model)
    @api.response(200, 'User details updated successfully')
    @api.response(400, 'You cannot modify email or password')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(500, 'Internal server error')
    def put(self, user_id):
        current_user = get_jwt_identity()
        claims = get_jwt()
        # If 'is_admin' is part of the identity payload
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        email = data.get('email')

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        # Logic to update user details, including email and password
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
       
        # Logic to update user details
        updated_user = facade.update_user(user_id, data)
        #check if user was updated
        if not updated_user:
            return {'error': 'Failed to update user'}, 500
       
        return {'id': current_user,
                'first_name': updated_user.first_name, 
                'last_name': updated_user.last_name, 
                'email': updated_user.email,
                'password': updated_user.password}, 200
    
@api.route('/amenities')
class AmenityCreate(Resource):
    @jwt_required()
    @api.response(201, 'Amenity successfully created')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @api.expect(amenity_model)  # Attach the model to validate the request data
    def post(self):
        """Add a new amenity"""
        current_user = get_jwt_identity()  # Get the current user's identity from the JWT token
        claims = get_jwt()  # Get the claims (including is_admin) from the JWT token

        # Check if the user has admin privileges (is_admin claim should be True)
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403  # If not an admin, return 403 Forbidden

        # Get the amenity data from the request payload
        amenity_data = api.payload
        try:
            # Use facade to create the amenity
            new_amenity = facade.create_amenity(amenity_data)
            return {
                    'id': new_amenity.id,
                    'name': new_amenity.name,
                    'description': new_amenity.description}, 201
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:  # Catch all other exceptions
            return {'message': 'invalid input data'}, 400
        
@api.route('amenities/<amenity_id>')
class AmenityUpdate(Resource):
    @jwt_required()
    @api.expect(amenity_upadate_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Extract data from the request and update the amenity
        current_user = get_jwt_identity()
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}
        data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            if updated_amenity:
                return {'name': updated_amenity.name,
                        'description': updated_amenity.description}, 201
            return {'message': 'Amenity not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:  # Catch all other exceptions
            return {'message': str(e)}, 404