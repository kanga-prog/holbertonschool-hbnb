# api/v1/places.py

from flask_restx import Namespace, Resource, fields
from app.services import facade  # Importing the facade that holds the business logic
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Operations on places')

# Model for reviews
review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Review rating (1 to 5)'),
    'user_id': fields.String(required=False, description='ID of the user who wrote the review'),
    'place_id': fields.String(required=False, description='ID of the place being reviewed')
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
    'owner_id': fields.String(required=False, description='Owner\'s ID'),
    'amenities': fields.List(fields.String, required=False, description="List of Amenity IDs")
})

place_update_model = api.model('Place_update', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'owner_id': fields.String(required=False, description='Owner\'s ID'),
    'amenities': fields.List(fields.String, required=False, description="List of Amenity IDs")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        current_user = get_jwt_identity()
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
                'owner_id': new_place.owner_id,
                    }, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of places fetched successfully')
    def get(self):
        """Fetch all places"""
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        if not places:
            return {'error': 'No places found'}, 404
        return [{'id': place.id,
                'title': place.title,
                'descrpition': place.description, 
                'price': place.price, 
                'latitude': place.latitude, 
                'longitude' : place.longitude, 
                'owner' : place.owner.id, 
                'reviews' : place.reviews, 
                'amenities' : place.associated_amenities} for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details fetched successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        # Récupérer les amenities associées à la place
        amenities = []
        for amenity in place.associated_amenities:
            amenities.append({
                'id': amenity.id,
                'name': amenity.name,
                'description': amenity.description
            })
        
        # Récupérer les reviews associées à la place
        reviews = []
        for review in place.reviews:
            reviews.append({
                'id': review.id,
                'text': review.text,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format de date
            })

        return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'amenities': amenities,
                'reviews': reviews
            }, 200

    @jwt_required()    
    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        current_user = get_jwt_identity()
        claims = get_jwt()
        try:
            place = facade.get_place(place_id) # retreive the place
            if not place:
                return {'error': 'Place not found'}, 404
            if place.owner_id != current_user and not claims.get('is_admin', False): # check if the owner of the place is the current user or an admin
                return {'message': 'Unauthorized action'}, 403
            
            facade.update_place(place_id, place_data)
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 400
    
    @jwt_required()
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def delete(self, place_id):
        """Delete an existing place"""
        current_user = get_jwt_identity()  # Get the current user's identity from the JWT token
        claims = get_jwt()  # Get the claims (including is_admin) from the JWT token

        # Retrieve the place to be deleted
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404  # If place does not exist, return 404 Not Found

        # Check if the current user is the owner of the place or if the user is an admin
        if place.owner_id != current_user and not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403  # Return 403 Forbidden

        # Delete the place using the facade
        facade.delete_place(place_id)

        # Return a success message
        return {'message': 'Place deleted successfully'}, 200

@api.route('/<place_id>/reviews')
class Reviews(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review added successfully')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """Add a review for a place"""
        review_data = api.payload
        review_data['place_id'] = place_id  # Associate the review with the place_id
        current_user = get_jwt_identity()

        try:
            #check if the user is not the owner
            place = facade.get_place(place_id)
            if place.owner_id == current_user:
                return {'message': 'You cannot review your own place'}
            
            # check if the user has already reviewed the place
            if facade.has_user_reviewed_place(current_user, place_id):
                return {'message': 'You have already reviewed this place'}, 400
            
            # Call the facade to create the review
            new_review = facade.create_review(review_data)
            return {
                 'id': new_review.id,
                    'text': new_review.text,
                    'rating': new_review.rating,
                    'user_id': new_review.user_id,
                    'place_id': new_review.place_id
                }, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 400
        
    @api.response(200, 'List of reviews fetched successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)  # Récupérer le lieu par ID
            return [{'id': review.id,
                    'text': review.text,
                    'rating': review.rating} for review in reviews], 200
        except Exception as e:
            return {'message': 'Place not found'}, 404