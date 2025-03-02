import unittest
from app.api.v1 import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.app = create_app()  # Crée l'application Flask
        self.client = self.app.test_client()  # Crée un client pour interagir avec l'API

    def test_create_place(self):
        """Test pour créer un lieu"""
        response = self.client.post('/api/v1/places', json={
            "title": "Beautiful Beach House",
            "description": "A lovely place by the beach.",
            "price": 150.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": "owner-123",
            "amenities": ["amenity-1", "amenity-2"]
        })
        self.assertEqual(response.status_code, 201)  # Vérifie que le code de statut est 201
        self.assertIn('id', response.json)  # Vérifie que l'ID du lieu est retourné
        self.assertEqual(response.json['title'], "Beautiful Beach House")  # Vérifie le titre du lieu

    def test_create_place_invalid_data(self):
        """Test pour créer un lieu avec des données invalides"""
        response = self.client.post('/api/v1/places', json={
            "title": "",
            "description": "A beautiful place",
            "price": -100.0,  # Prix invalide
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": "owner-123"
        })
        self.assertEqual(response.status_code, 400)  # Vérifie que le code de statut est 400
        self.assertEqual(response.json['message'], "Price must be a positive number.")  # Vérifie le message d'erreur

    def test_get_all_places(self):
        """Test pour récupérer tous les lieux"""
        response = self.client.get('/api/v1/places')
        self.assertEqual(response.status_code, 200)  # Vérifie que le code de statut est 200
        self.assertGreater(len(response.json), 0)  # Vérifie que des lieux sont retournés

    def test_get_place(self):
        """Test pour récupérer un lieu spécifique par son ID"""
        # Crée un lieu pour tester
        create_response = self.client.post('/api/v1/places', json={
            "title": "Mountain View Cabin",
            "description": "A cozy cabin in the mountains.",
            "price": 200.0,
            "latitude": 35.3733,
            "longitude": -118.5982,
            "owner_id": "owner-123"
        })
        place_id = create_response.json['id']

        # Récupère le lieu par son ID
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)  # Vérifie que le code de statut est 200
        self.assertEqual(response.json['title'], "Mountain View Cabin")  # Vérifie le titre du lieu

    def test_get_place_not_found(self):
        """Test pour récupérer un lieu qui n'existe pas"""
        response = self.client.get('/api/v1/places/unknown-id')
        self.assertEqual(response.status_code, 404)  # Vérifie que le code de statut est 404
        self.assertEqual(response.json['message'], "Place not found")  # Vérifie le message d'erreur

    def test_update_place(self):
        """Test pour mettre à jour un lieu"""
        # Crée un lieu pour le test
        create_response = self.client.post('/api/v1/places', json={
            "title": "Cozy Apartment",
            "description": "A small but comfortable apartment.",
            "price": 120.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": "owner-123"
        })
        place_id = create_response.json['id']

        # Mise à jour du lieu
        update_response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Cozy Apartment",
            "description": "Now with better amenities.",
            "price": 150.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": "owner-123"
        })
        self.assertEqual(update_response.status_code, 200)  # Vérifie que le code de statut est 200
        self.assertEqual(update_response.json['message'], "Place updated successfully")  # Vérifie le message de succès

    def test_add_review_to_place(self):
        """Test pour ajouter une critique à un lieu"""
        # Crée un lieu pour tester
        create_response = self.client.post('/api/v1/places', json={
            "title": "Lakeside Cottage",
            "description": "A beautiful cottage by the lake.",
            "price": 180.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": "owner-123"
        })
        place_id = create_response.json['id']

        # Ajouter une critique au lieu
        response = self.client.post(f'/api/v1/places/{place_id}/reviews', json={
            "text": "Amazing place to relax!",
            "rating": 5,
            "user_id": "user-123",
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 201)  # Vérifie que le code de statut est 201
        self.assertIn('id', response.json)  # Vérifie que l'ID de la critique est retourné

    def test_get_reviews_for_place(self):
        """Test pour récupérer les critiques d'un lieu"""
        # Crée un lieu et une critique pour le test
        create_response = self.client.post('/api/v1/places', json={
            "title": "Sunny Villa",
            "description": "A villa with a fantastic view.",
            "price": 300.0,
            "latitude": 36.7783,
            "longitude": -119.4179,
            "owner_id": "owner-123"
        })
        place_id = create_response.json['id']
        self.client.post(f'/api/v1/places/{place_id}/reviews', json={
            "text": "Wonderful experience!",
            "rating": 5,
            "user_id": "user-123",
            "place_id": place_id
        })

        # Récupère les critiques pour le lieu
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)  # Vérifie que le code de statut est 200
        self.assertGreater(len(response.json), 0)  # Vérifie qu'il y a des critiques retournées

if __name__ == '__main__':
    unittest.main()
