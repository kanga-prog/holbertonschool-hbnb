""" method creat a review"""
def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user:
            raise ValueError("The specified user does not exist.")
        if not place:
            raise ValueError("The specified place does not exist.")
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        return review

"""method get a review"""
    def get_review(self, review_id):
        return self.review_repo.get(review_id)

"""methode get all a reviews"""
    def get_all_reviews(self):
        return self.review_repo.get_all()

""" method get a review by place """
    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("The specified place does not exist.")
        return self.review_repo.get_reviews_by_place(place_id)

""" methode a update review"""
    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if review_data.get('text'):
            review.text = review_data['text']
        if review_data.get('rating') is not None:
            if not (1 <= review_data['rating'] <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            review.rating = review_data['rating']
        self.review_repo.update(review_id, review)
        return review

""" methode delete"""
    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return
