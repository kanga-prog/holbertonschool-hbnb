import unittest
from .api.v1 import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.app = create_app()  # Crée l'application Flask
        self.client = self.app.test_client()  # Crée un client pour interagir avec l'API

    def test_create_amenity(self):
        """Test pour créer une nouvelle commodité"""
        response = self.client.post('/api/v1/amenities', json={
            "name": "Swimming Pool"
        })
        self.assertEqual(response.status_code, 201)  # Vérifie que la commodité est créée avec succès
        self.assertIn('id', response.json)  # Vérifie que l'ID de la commodité est retourné
        self.assertEqual(response.json['name'], "Swimming Pool")  # Vérifie le nom de la commodité

    def test_create_amenity_invalid_data(self):
        """Test pour créer une commodité avec des données invalides"""
        response = self.client.post('/api/v1/amenities', json={})
        self.assertEqual(response.status_code, 400)  # Vérifie que le code de statut est 400
        self.assertEqual(response.json['message'], "Invalid input data")  # Vérifie le message d'erreur

    def test_get_all_amenities(self):
        """Test pour récupérer toutes les commodités"""
        response = self.client.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)  # Vérifie que le code de statut est 200
        self.assertGreater(len(response.json), 0)  # Vérifie qu'il y a des commodités retournées

    def test_get_amenity(self):
        """Test pour récupérer une commodité spécifique par ID"""
        # Crée une commodité pour tester
        create_response = self.client.post('/api/v1/amenities', json={
            "name": "Gym"
        })
        amenity_id = create_response.json['id']

        # Récupère la commodité par son ID
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)  # Vérifie que le code de statut est 200
        self.assertEqual(response.json['name'], "Gym")  # Vérifie le nom de la commodité

    def test_get_amenity_not_found(self):
        """Test pour récupérer une commodité qui n'existe pas"""
        response = self.client.get('/api/v1/amenities/unknown-id')
        self.assertEqual(response.status_code, 404)  # Vérifie que le code de statut est 404
        self.assertEqual(response.json['message'], "Amenity not found")  # Vérifie le message d'erreur

    def test_update_amenity(self):
        """Test pour mettre à jour une commodité"""
        # Crée une commodité pour le test
        create_response = self.client.post('/api/v1/amenities', json={
            "name": "Sauna"
        })
        amenity_id = create_response.json['id']

        # Mise à jour de la commodité
        update_response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Luxury Sauna"
        })
        self.assertEqual(update_response.status_code, 200)  # Vérifie que la commodité est mise à jour avec succès
        self.assertEqual(update_response.json['name'], "Luxury Sauna")  # Vérifie le nom mis à jour

if __name__ == '__main__':
    unittest.main()
