from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import json

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=True, description='Description of the amenity')
    })

amenity_update_model = api.model('Amenity_upadate', {
    'description': fields.String(required=True, description='Description of the amenity')
    })

@api.route('/amenities')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
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

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 
            'name': amenity.name,
            'description': amenity.description} for amenity in amenities], 200

@api.route('/amenities/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Fetch a specific amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return {
                    'id': amenity.id,
                    'name': amenity.name,
                    'description': amenity.description}, 201
        return {'message': 'Amenity not found'}, 404

    @api.expect(amenity_update_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Extract data from the request and update the amenity
        data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            if updated_amenity:
                return {
                        'id': updated_amenity.id,
                        'name': updated_amenity.name}, 201
            return {'message': 'Amenity not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:  # Catch all other exceptions
            return {'message': str(e)}, 404

# Task 4
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        amenity_data = request.json

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return { 'id': new_amenity.id,
                    'name': new_amenity.name,
                    'description': new_amenity.description }, 201
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e: # Catch all other exceptions
            return {'message': 'Invalid input data'}, 400

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to update an amenity
        data = request.json

        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            return { 'id': updated_amenity.id,
                    'name': updated_amenity.name,
                    'description': updated_amenity.description }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Logic to update the place
        data = request.json

        try:
            updated_place = facade.update_place(place_id, data)
            return {
                    'id': updated_place.id,
                    'title': updated_place.title,
                    'description': updated_place.description,
                    'price': updated_place.price,
                    'latitude': updated_place.latitude,
                    'longitude': updated_place.longitude,
                    'owner_id': updated_place.owner_id }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500
