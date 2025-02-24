# tests/test_amenity.py

from app.models.amenity import Amenity

def test_amenity_creation():
    # Création d'un équipement
    amenity = Amenity(name="Wi-Fi")
    
    # Vérification que le nom de l'équipement est bien "Wi-Fi"
    assert amenity.name == "Wi-Fi"
    
    print("Amenity creation test passed!")

# Lancer le test
if __name__ == "__main__":
    test_amenity_creation()
