import unittest
import sys
sys.path.append("..")
from app.api.v1 import create_app
from app.services import facade

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def check_redirection(self, response):
        """Vérifie si une redirection a eu lieu et affiche l'URL de redirection"""
        if response.status_code == 308:
            redirect_url = response.headers.get('Location')
            print(f"Redirection vers l'URL: {redirect_url}")
            self.assertIn('/api/v1/users', redirect_url)  # Assurez-vous que la redirection va vers la bonne route
    
    def test_create_user(self):
        """Test pour créer un nouvel utilisateur"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonderland",
            "email": "alice@example.com",
            "password": "motdepasse"
        })

        # Vérification du code de statut et suppression de la vérification de redirection
        self.assertEqual(response.status_code, 201)  # Réponse attendue : 201, pas 200
        self.assertIn('id', response.json)  # Vérifie que l'ID est bien retourné

    def test_create_user_invalid_data(self):
        """Test pour créer un utilisateur avec des données invalides"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": ""
        })

        # Vérification du code de statut
        self.assertEqual(response.status_code, 400)  # Réponse attendue : 400
        self.assertIn('message', response.json)  # Assurez-vous que le message d'erreur est présent

    def test_create_user_duplicate_email(self):
        """Test pour essayer de créer un utilisateur avec un email déjà utilisé"""
        # Crée un utilisateur initialement
        self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonderland",
            "email": "alice@example.com",
            "password": "motdepasse"
        })

        # Essayons de créer un autre utilisateur avec le même email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "alice@example.com",  # Email dupliqué
            "password": "motdepasse"
        })

        self.assertEqual(response.status_code, 400)  # Réponse attendue : 400 pour l'email dupliqué

    def test_get_user(self):
        """Test pour récupérer les détails d'un utilisateur"""
        # Créons un utilisateur pour le test
        user_data = {
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "charlie.brown@example.com",
            "password": "motdepasse"
        }
        create_response = self.client.post('/api/v1/users/', json=user_data)
        user_id = create_response.get_json().get('id')  # Récupère l'ID du nouvel utilisateur

        # Récupérons les détails de l'utilisateur
        response = self.client.get(f'/api/v1/users/{user_id}')
        
        self.assertEqual(response.status_code, 200)  # Vérifie que la réponse est OK
        self.assertEqual(response.json['first_name'], user_data["first_name"])  # Vérifie le prénom
        self.assertEqual(response.json['last_name'], user_data["last_name"])  # Vérifie le nom de famille

    def test_get_user_not_found(self):
        """Test pour récupérer un utilisateur inexistant"""
        response = self.client.get('/api/v1/users/unknown-id')

        self.assertEqual(response.status_code, 404)  # Réponse attendue : 404 pour un utilisateur introuvable
        self.assertEqual(response.json['error'], "User not found")  # Message d'erreur attendu

    def test_update_user(self):
        """Test pour mettre à jour un utilisateur"""
        # Crée un utilisateur pour mettre à jour
        user_data = {
            "first_name": "David",
            "last_name": "Smith",
            "email": "david.smith@example.com",
            "password": "motdepasse"
        }
        create_response = self.client.post('/api/v1/users/', json=user_data)
        user_id = create_response.get_json().get('id')

        # Mise à jour des informations de l'utilisateur
        updated_data = {
            "first_name": "David",
            "last_name": "Smithson",
            "email": "david.smithson@example.com",
            "password": "motdepasse"
        }
        update_response = self.client.put(f'/api/v1/users/{user_id}', json=updated_data)

        self.assertEqual(update_response.status_code, 200)  # Vérifie que la mise à jour a réussi
        self.assertEqual(update_response.json['last_name'], "Smithson")  # Vérifie le nouveau nom

    def test_update_user_not_found(self):
        """Test pour essayer de mettre à jour un utilisateur inexistant"""
        updated_data = {
            "first_name": "Nonexistent",
            "last_name": "User",
            "email": "nonexistent.user@example.com",
            "password": "motdepasse"
        }
        response = self.client.put('/api/v1/users/unknown-id', json=updated_data)

        self.assertEqual(response.status_code, 404)  # Réponse attendue : 404 pour un utilisateur inexistant
        self.assertEqual(response.json['error'], "User not found")  # Message d'erreur attendu
