# tests/test_place.py

from app.models.user import User
from app.models.place import Place

def test_place_creation():
    # Création d'un utilisateur (propriétaire) avec un ID explicite
    owner = User(id="12345", first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    
    # Création d'un lieu avec cet utilisateur comme propriétaire
    place = Place(
        title="Appartement à Paris",
        description="Un bel appartement situé en plein cœur de Paris.",
        price=120.0,
        latitude=48.8566,
        longitude=2.3522,
        owner=owner  # Propriétaire du lieu
    )
    
    # Vérification que le lieu a été correctement créé
    assert place.title == "Appartement à Paris"
    assert place.owner.first_name == "Alice"
    assert place.owner.last_name == "Smith"
    assert place.owner.email == "alice.smith@example.com"
    
    print("Test de création du lieu passé avec succès!")

# Exécution du test
test_place_creation()
