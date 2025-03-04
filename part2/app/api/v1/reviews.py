from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('Review_update', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
})

@api.route('/reviews')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return {'id': new_review.id,
                    'text': new_review.text,
                    'rating': new_review.rating,
                    'user_id': new_review.user.id,
                    'place_id': new_review.place.id}, 201
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

@api.route('/reviews/<review_id>')
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
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'message': 'Review not found'}
            return {'id': updated_review.id,
                    'text': updated_review.text,
                    'rating': updated_review.rating}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:  # Catch all other exceptions
            return {'message': str(e)}, 400
