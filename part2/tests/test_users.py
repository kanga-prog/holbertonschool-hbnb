import unittest
from app import create_app
from app.services import facade

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.app = create_app()  # Crée l'application Flask
        self.client = self.app.test_client()  # Crée un client pour interagir avec l'API

    def test_create_user(self):
        """Test pour créer un nouvel utilisateur"""
        response = self.client.post('/api/v1/users', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)  # Vérifie que le code de statut est 201
        self.assertIn('id', response.json)  # Vérifie que l'ID du nouvel utilisateur est retourné
        self.assertEqual(response.json['first_name'], "John")  # Vérifie que le prénom est correct

    def test_create_user_invalid_data(self):
        """Test pour créer un utilisateur avec des données invalides"""
        response = self.client.post('/api/v1/users', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)  # Vérifie que le code de statut est 400
        self.assertEqual(response.json['error'], "Invalid input data")  # Vérifie le message d'erreur

    def test_create_user_duplicate_email(self):
        """Test pour essayer de créer un utilisateur avec un email déjà utilisé"""
        # Crée un utilisateur initialement
        self.client.post('/api/v1/users', json={
            "first_name": "Alice",
            "last_name": "Wonderland",
            "email": "alice@example.com"
        })

        # Essayons de créer un autre utilisateur avec le même email
        response = self.client.post('/api/v1/users', json={
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "alice@example.com"
        })
        self.assertEqual(response.status_code, 400)  # Vérifie que le code de statut est 400
        self.assertEqual(response.json['error'], "Email already registered")  # Vérifie le message d'erreur

    def test_get_user(self):
        """Test pour récupérer les détails d'un utilisateur"""
        # Créons un utilisateur pour le test
        user_data = {
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "charlie.brown@example.com"
        }
        create_response = self.client.post('/api/v1/users', json=user_data)
        user_id = create_response.json['id']

        # Récupérons les détails de l'utilisateur
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)  # Vérifie que le code de statut est 200
        self.assertEqual(response.json['first_name'], user_data["first_name"])  # Vérifie que le prénom est correct
        self.assertEqual(response.json['last_name'], user_data["last_name"])  # Vérifie que le nom de famille est correct

    def test_get_user_not_found(self):
        """Test pour récupérer un utilisateur inexistant"""
        response = self.client.get('/api/v1/users/unknown-id')
        self.assertEqual(response.status_code, 404)  # Vérifie que le code de statut est 404
        self.assertEqual(response.json['error'], "User not found")  # Vérifie le message d'erreur

    def test_update_user(self):
        """Test pour mettre à jour un utilisateur"""
        # Crée un utilisateur pour mettre à jour
        user_data = {
            "first_name": "David",
            "last_name": "Smith",
            "email": "david.smith@example.com"
        }
        create_response = self.client.post('/api/v1/users', json=user_data)
        user_id = create_response.json['id']

        # Mise à jour des informations de l'utilisateur
        updated_data = {
            "first_name": "David",
            "last_name": "Smithson",
            "email": "david.smithson@example.com"
        }
        update_response = self.client.put(f'/api/v1/users/{user_id}', json=updated_data)
        self.assertEqual(update_response.status_code, 200)  # Vérifie que le code de statut est 200
        self.assertEqual(update_response.json['last_name'], "Smithson")  # Vérifie que le nom a été mis à jour

    def test_update_user_not_found(self):
        """Test pour essayer de mettre à jour un utilisateur inexistant"""
        updated_data = {
            "first_name": "Nonexistent",
            "last_name": "User",
            "email": "nonexistent.user@example.com"
        }
        response = self.client.put('/api/v1/users/unknown-id', json=updated_data)
        self.assertEqual(response.status_code, 404)  # Vérifie que le code de statut est 404
        self.assertEqual(response.json['error'], "User not found")  # Vérifie le message d'erreur

if __name__ == '__main__':
    unittest.main()
