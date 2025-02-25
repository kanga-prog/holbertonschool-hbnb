#!/usr/bin/python3
from app.models.user import User

def test_user_creation():
    # Création d'un utilisateur
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    
    # Vérification des attributs
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # La valeur par défaut est False
    
    print("Test de création d'utilisateur passé avec succès!")

# Lancer le test
if __name__ == "__main__":
    test_user_creation()
