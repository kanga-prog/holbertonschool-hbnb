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
