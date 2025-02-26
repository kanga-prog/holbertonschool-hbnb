# app/serrvices/facade.py

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

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

    def create_place(self, place_data):
        # Creates a place (property)
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("The specified owner does not exist.")
        
        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner
            )
        except ValueError as e:
            raise ValueError(f"Error while creating the place: {str(e)}")
        
        # Adding amenities to the place
        amenities = [self.amenity_repo.get(amenity_id) for amenity_id in place_data.get('amenities', [])]
        for amenity in amenities:
            place.add_amenity(amenity)
        
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
        # Updates an existing place
        place = self.place_repo.get(place_id)
        if not place:
            return None  # Place not found
        # Updating the place's details
        if place_data.get('title'):
            place.title = place_data['title']
        if place_data.get('description'):
            place.description = place_data['description']
        if place_data.get('price') is not None:
            place.price = place_data['price']
        if place_data.get('latitude') is not None:
            place.latitude = place_data['latitude']
        if place_data.get('longitude') is not None:
            place.longitude = place_data['longitude']
        # Adding or updating amenities
        if place_data.get('amenities'):
            amenities = [self.amenity_repo.get(amenity_id) for amenity_id in place_data['amenities']]
            place.amenities = amenities
        self.place_repo.update(place_id, place)
        return place
