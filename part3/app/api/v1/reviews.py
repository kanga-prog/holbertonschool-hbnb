from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')
api.add_resource(Review_list, '/')
api.add_resource(Review_resource, '/<int:review_id>')

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
    @jwt_required()
    def post(self):
        """Create a new review"""
        review_data = api.payload
        #task 3
        current_user = get_jwt_identity()
        place_id = review_data.get('place_id')
        place = facade.get_place(place_id)
        if place.owner_id == current_user:
            return {'error': 'You cannot review your own place'}, 400
        if facade.has_user_already_reviewed(current_user, place_id):
            return {'error': 'You have already reviewed this place'}, 400
        review_data['user_id'] = current_user
        # fin task 3
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
    @jwt_required()
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
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        review_data = api.payload
        # task 3
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if review.user_id != current_user:
            return {'error': 'Action not authorized'}, 403
        # fin task 3
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

# task 3 create method delete
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if review.user_id != current_user:
            return {'error': 'Action not allowed'}, 400
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            return {'message': str(e)}, 404
