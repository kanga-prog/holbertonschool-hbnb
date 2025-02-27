# api/v1/places.py

from flask_restx import Namespace, Resource, fields
from app.services import facade  # Importing the facade that holds the business logic

api = Namespace('places', description='Operations on places')

# Model for reviews
review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Review rating (1 to 5)'),
    'user_id': fields.String(required=True, description='ID of the user who wrote the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

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
    'amenities': fields.List(fields.String, required=False, description="List of Amenity IDs")
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
                'owner_id': new_place.owner.id,
                    }, 201
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
                'longitude': place.longitude,
                'reviews': place.reviews})
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
            reviews = [{'id': review.id,
                        'text': review.text,
                        'rating': review.rating,
                        'user_id': review.user.id} for review in place.reviews]
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': owner,
                'amenities': amenities,
                'reviews': reviews
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

@api.route('/<place_id>/reviews')
class Reviews(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review added successfully')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """Add a review for a place"""
        review_data = api.payload
        review_data['place_id'] = place_id  # Associate the review with the place_id
        try:
        # Call the facade to create the review
            new_review = facade.create_review(review_data)
            return {
                 'id': new_review.id,
                    'text': new_review.text,
                    'rating': new_review.rating,
                    'user_id': new_review.user.id,
                    'place_id': new_review.place.id
                }, 201
        except ValueError as e:
            return {'message': str(e)}, 400