# app/serrvices/facade.py

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
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

    def create_amenity(self, amenity_data):
        # Create a new amenity and add it to the repository
        amenity = Amenity(name=amenity_data["name"])
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
