from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=False, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('Review_update', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()
        place_id = review_data['place_id']
        review_data['user_id'] = current_user
        #check if the user is not the owner
        place = facade.get_place(place_id)
        if place.owner_id == current_user:
            return {'message': 'You cannot review your own place'}
            
        # check if the user has already reviewed the place
        place_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for existing_review in place_reviews:
            if existing_review.user_id == current_user: # dont make it a dict or you wont be able to make many reviews
                return {'error': 'You have already reviewed this place'}, 400

        try:            
            new_review = facade.create_review(review_data)
            return {'id': new_review.id,
                    'text': new_review.text,
                    'rating': new_review.rating,
                    'user_id': new_review.user_id,
                    'place_id': new_review.place_id}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:  # Catch all other exceptions
            return {'message': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id,
                 'text': review.text,
                 'rating': review.rating,
                 'user_id': review.user.id,
                 'place_id': review.place.id} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by its ID"""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'message': 'Review not found'}
            return {'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id,
                    'place_id': review.place.id}, 200
        except Exception as e:  # Catch all other exceptions
            return {'message': 'Review not found'}, 404
        
    @api.expect(review_update_model)
    @jwt_required()
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        review_data = api.payload
        current_user = get_jwt_identity()
        try:
            #retrieve the review by its id
            review = facade.get_review(review_id)
            if not review:
                return {'message': 'Review not found'}, 404

            #check if the current user is the author of he review
            if review.user_id != current_user:
                return {'message' : 'Unauthorized action'}, 403
            
            updated_review = facade.update_review(review_id, review_data)
            return {'id': updated_review.id,
                    'text': updated_review.text,
                    'rating': updated_review.rating}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:  # Catch all other exceptions
            return {'message': str(e)}, 400


    @jwt_required()  # Ensure the user is authenticated
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review by its ID"""
        current_user = get_jwt_identity()  # Get the currently authenticated user's ID

        try:
            # Fetch the review from the database using the review_id
            review = facade.get_review_by_id(review_id)
            if not review:
                return {'message': 'Review not found'}, 404

            # Check if the current user is the author of the review
            if review.user.id != current_user:
                return {'message': 'Unauthorized action'}, 403  # Return a 403 if the user is not the author

            # Proceed with deleting the review if the user is the author
            facade.delete_review(review_id)

            return {'message': 'Review deleted successfully'}, 200

        except ValueError as e:
            return {'message': 'Review not found'}, 404  # Return a 404 if the review doesn't exist
        except Exception as e:
            return {'message': str(e)}, 400  # Catch any other errors and return a 400