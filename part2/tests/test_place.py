# tests/test_place.py

from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation():
    # Création d'un utilisateur (propriétaire)
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    
    # Création d'un lieu (Place)
    place = Place(
        title="Cozy Apartment", 
        description="A nice place to stay", 
        price=100, 
        latitude=37.7749, 
        longitude=-122.4194, 
        owner=owner
    )

    # Ajout d'une revue
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    # Vérifications
    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    assert place.reviews[0].rating == 5
    print("Place creation and review test passed!")

# Lancer le test
if __name__ == "__main__":
    test_place_creation()
