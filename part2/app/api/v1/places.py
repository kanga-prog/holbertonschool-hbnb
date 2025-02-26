# api/v1/places.py

from flask_restx import Namespace, Resource, fields
from app.services import facade  # Importing the facade that holds the business logic

api = Namespace('places', description='Operations on places')

# Model for amenities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

# Model for users (owners)
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='Owner\'s first name'),
    'last_name': fields.String(description='Owner\'s last name'),
    'email': fields.String(description='Owner\'s email')
})

# Model for places
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='Owner\'s ID'),
    'amenities': fields.List(fields.String, required=True, description="List of Amenity IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            # Call facade method to create a place
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id,}, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of places fetched successfully')
    def get(self):
        """Fetch all places"""
        places = facade.get_all_places()
        result = []
        for place in places:
            result.append({
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
            })
        return result, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details fetched successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            amenities = [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities]
            owner = {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            }
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': owner,
                'amenities': amenities
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return {'message': str(e)}, 404
        except Exception as e:
            return {'message': str(e)}, 400
