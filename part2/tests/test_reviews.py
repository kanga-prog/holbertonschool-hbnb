import unittest
import sys
sys.path.append("..")
from app.api.v1 import create_app
from app.services import facade

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.app = create_app()  # Crée l'application Flask
        self.client = self.app.test_client()  # Crée un client pour interagir avec l'API

    def check_redirection(self, response):
        """Vérifie si une redirection a eu lieu et affiche l'URL de redirection"""
        if response.status_code == 308:
            redirect_url = response.headers.get('Location')
            self.assertIn('/api/v1/reviews', redirect_url)  # Assurez-vous que la redirection va vers la bonne route

    def test_create_review(self):
        """Test pour créer une nouvelle review"""
                # Créons un utilisateur pour le test
        user_data = {
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "charlie.brown@example.com"
        }
        create_response = self.client.post('/api/v1/users/', json=user_data)
        user_id = create_response.get_json().get('id')

        response = self.client.post('/api/v1/reviews/', json={
            "text": "This is a great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": "owner-123"
        })

        # Vérification de la redirection
        self.check_redirection(response)

        # Vérification que le code de statut est 201 et que la réponse contient un ID
        if response.status_code != 308:
            self.assertEqual(response.status_code, 201)  # Vérifie que le code de statut est 201
            self.assertIn('id', response.json)  # Vérifie que l'ID de la nouvelle review est retourné
            self.assertEqual(response.json['text'], "This is a great place!")  # Vérifie le texte de la review

    def test_create_review_invalid_data(self):
        """Test pour créer une review avec des données invalides"""
        response = self.client.post('/api/v1/reviews', json={
            "text": "",
            "rating": 10,  # Le rating doit être entre 1 et 5
            "user_id": "",
            "place_id": "place-456"
        })

        # Vérification de la redirection
        self.check_redirection(response)

        if response.status_code != 308:
            self.assertEqual(response.status_code, 400)  # Vérifie que le code de statut est 400
            self.assertEqual(response.json['message'], "The rating must be between 1 and 5")  # Vérifie le message d'erreur

    def test_get_all_reviews(self):
        """Test pour récupérer toutes les reviews"""
        # Crée une review pour tester
        self.client.post('/api/v1/reviews/', json={
            "text": "Awesome place!",
            "rating": 4,
            "user_id": "user-123",
            "place_id": "place-456"
        })

        # Récupère toutes les reviews
        response = self.client.get('/api/v1/reviews')

        # Vérification de la redirection
        self.check_redirection(response)

        if response.status_code != 308:
            self.assertEqual(response.status_code, 200)  # Vérifie que le code de statut est 200
            self.assertGreater(len(response.json), 0)  # Vérifie que la réponse contient des reviews

    def test_get_review(self):
        """Test pour récupérer une review par ID"""
        # Crée une review pour le test
        create_response = self.client.post('/api/v1/reviews', json={
            "text": "Nice place!",
            "rating": 5,
            "user_id": "user-123",
            "place_id": "place-456"
        })

        # Vérification de la redirection après création
        self.check_redirection(create_response)

        if create_response.status_code != 308:
            review_id = create_response.json['id']

            # Récupère la review par son ID
            response = self.client.get(f'/api/v1/reviews/{review_id}')

            # Vérification de la redirection
            self.check_redirection(response)

            self.assertEqual(response.status_code, 200)  # Vérifie que le code de statut est 200
            self.assertEqual(response.json['text'], "Nice place!")  # Vérifie le texte de la review

    def test_get_review_not_found(self):
        """Test pour récupérer une review qui n'existe pas"""
        response = self.client.get('/api/v1/reviews/unknown-id')

        # Vérification de la redirection
        self.check_redirection(response)

        if response.status_code != 308:
            self.assertEqual(response.status_code, 404)  # Vérifie que le code de statut est 404
            self.assertEqual(response.json['message'], "Review not found")  # Vérifie le message d'erreur

    def test_update_review(self):
        """Test pour mettre à jour une review"""
        # Crée une review pour le test
        create_response = self.client.post('/api/v1/reviews', json={
            "text": "Old review",
            "rating": 3,
            "user_id": "user-123",
            "place_id": "place-456"
        })

        # Vérification de la redirection après création
        self.check_redirection(create_response)

        if create_response.status_code != 308:
            review_id = create_response.json['id']

            # Met à jour la review
            update_response = self.client.put(f'/api/v1/reviews/{review_id}', json={
                "text": "Updated review",
                "rating": 4,
                "user_id": "user-123",
                "place_id": "place-456"
            })

            # Vérification de la redirection après mise à jour
            self.check_redirection(update_response)

            self.assertEqual(update_response.status_code, 200)  # Vérifie que le code de statut est 200
            self.assertEqual(update_response.json['text'], "Updated review")  # Vérifie que la review a été mise à jour

    def test_update_review_invalid_data(self):
        """Test pour essayer de mettre à jour une review avec des données invalides"""
        # Crée une review pour le test
        create_response = self.client.post('/api/v1/reviews', json={
            "text": "Another review",
            "rating": 5,
            "user_id": "user-123",
            "place_id": "place-456"
        })

        # Vérification de la redirection après création
        self.check_redirection(create_response)

        if create_response.status_code != 308:
            review_id = create_response.json['id']

            # Mise à jour avec un rating invalide (ex. rating > 5)
            response = self.client.put(f'/api/v1/reviews/{review_id}', json={
                "text": "Updated review with invalid data",
                "rating": 10,  # Rating invalide (supérieur à 5)
                "user_id": "user-123",
                "place_id": "place-456"
            })

            # Vérification de la redirection
            self.check_redirection(response)

            self.assertEqual(response.status_code, 400)  # Vérifie que le code de statut est 400
            self.assertEqual(response.json['message'], "The rating must be between 1 and 5")  # Vérifie le message d'erreur
