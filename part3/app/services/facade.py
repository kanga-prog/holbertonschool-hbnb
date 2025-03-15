# app/serrvices/facade.py
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.amenity_repository import AmenityRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()


    def update_user(self, user_id, user_data):
        updated_user = self.user_repo.update(user_id, user_data)
        if not updated_user:
            return None  # L'utilisateur n'a pas été trouvé
        return updated_user
    
    def delete_user(self, user_id):
        """deletes an user"""
        return self.user_repo.delete(user_id)

    def create_amenity(self, amenity_data):
        # Create a new amenity and add it to the repository
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Retrieve an amenity by its ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Retrieve all amenities in the repository
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Update an amenity's details by its ID
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.name = amenity_data.get('name', amenity.name)
            return amenity
        return None
    
    def delete_amenity(self, amenity_id):
        """deletes an user"""
        return self.amenity_repo.delete(amenity_id)

    def create_place(self, place_data):
        # Creates a place (property)
        place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id']
            )
        # Add the place to the in-memory repository
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Retrieves a place by ID
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Retrieves all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""
        return self.place_repo.update(place_id, place_data)
    
    def delete_place(self, place_id):
        """Deletes a review by its ID."""
        self.place_repo.delete(place_id)
    
    def create_review(self, review_data):
        """Créer un nouvel avis"""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review
        
    def get_review(self, review_id):
        """Récupérer un avis par ID"""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return review

    def get_all_reviews(self):
        """Récupérer tous les avis"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Récupérer tous les avis pour un lieu spécifique"""
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        """Mettre à jour un avis existant"""
        review = self.get_review(review_id)
        review.text = review_data.get('text', review.text)
        review.rating = review_data.get('rating', review.rating)
        review.validate_review()
        review.save()  # Sauvegarder les modifications dans l'InMemoryRepository
        return review

    def delete_review(self, review_id):
        """Deletes a review by its ID."""
        self.review_repo.delete(review_id)