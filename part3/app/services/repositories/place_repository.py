# repositories/place_repository.py
from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity
from app.models.review import Review

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def add(self, place):
        """Ajouter un lieu"""
        db.session.add(place)
        db.session.commit()

    def get(self, place_id):
        """Récupérer un lieu par son ID"""
        return self.model.query.get(place_id)

    def update(self, place_id, updated_data):
        """Mettre à jour un lieu"""
        place = self.get(place_id)
        if place:
            for key, value in updated_data.items():
                setattr(place, key, value)
            # Gestion des amenities
            if 'amenities' in updated_data:
                amenities = []
                for amenity_id in updated_data['amenities']:
                    amenity = Amenity.query.get(amenity_id)
                    if amenity:
                        amenities.append(amenity)
                    else:
                        raise ValueError(f"Amenity with id {amenity_id} not found")
                    
                place.associated_amenities = amenities
                
            if 'reviews' in updated_data:
                reviews = []
                for review_data in updated_data['reviews']:
                    # Récupérer les informations de la review
                    rating = review_data.get('rating')
                    text = review_data.get('text')  # Maintenant nous récupérons 'text' au lieu de 'comment'
                    user_id = review_data.get('user_id')
                    # Créer une nouvelle review
                    review = Review(rating=rating, text=text, place_id=place.id, user_id=user_id)
                    reviews.append(review)
        
                # Associer les reviews à la place
                place.reviews = reviews
            db.session.commit()
        return place

    def delete(self, place_id):
        """Supprimer un lieu"""
        place = self.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
        return place

    def get_all(self):
        """Récupérer tous les lieux"""
        return self.model.query.all()
