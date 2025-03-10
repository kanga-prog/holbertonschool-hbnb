import unittest
import sys
sys.path.append("..")
from app import create_app
from app.services import facade

class TestPlaceEndpoints(unittest.TestCase):
    """Test Class for testing places endpoints"""
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def check_redirection(self, response):
        """Vérifie si une redirection a eu lieu et affiche l'URL de redirection"""
        if response.status_code == 308:
            redirect_url = response.headers.get('Location')
            print(f"Redirection vers l'URL: {redirect_url}")
            self.assertIn('/api/v1/places', redirect_url)  # Assurez-vous que la redirection va vers la bonne route

    def test_create_place(self):
        # Success create a new place
        response0 = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonderland",
            "email": "alice@example.com",
            "password": "motdepasse"
        })
        
        owner_id = response0.get_json().get('id')
        print(owner_id)
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 75.0,
            "latitude": 47,
            "longitude": 14,
            "owner": owner_id,
            "reviews": [],
            "amenities": []
        })
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        print(data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], "Cozy Apartment")
        self.assertEqual(data['price'], 75.0)
        self.assertEqual(data['latitude'], 47)
        self.assertEqual(data['longitude'], 14)
        self.assertEqual(data['owner'], "owner_id")

    def test_create_place_invalid_data(self):
        # Fail creation of a new place with incorrect information format
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "",
            "price": -50.0,
            "latitude": "invalid",
            "longitude": None,
            "owner": "",
            "reviews": "",
            "amenities": "not_a_list"
        })
        self.check_redirection(response)
        
        if response.status_code == 308:
            response = self.client.get(response.headers['Location'])  # Suivi de la redirection
        
        self.assertEqual(response.status_code, 404)

    def test_create_out_of_range(self):
        # Fail creation of a new place with latitude and longitude out of range
        response = self.client.post('/api/v1/places/', json={
            "title": "villa",
            "description": "sea view",
            "price": 3000000,
            "latitude": 100,  # Latitude invalide (au-delà de 90)
            "longitude": 190,  # Longitude invalide (au-delà de 180)
            "owner": "fc042da8-4a0c-48c4-ab16-bd3217830863",
            "reviews": [],
            "amenities":[]
        })
        self.check_redirection(response)
        
        if response.status_code == 308:
            response = self.client.get(response.headers['Location'])  # Suivi de la redirection
        
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        # Success/Fail retrieve all the places
        response = self.client.get('/api/v1/places/')
        self.check_redirection(response)
        
        if response.status_code == 308:
            response = self.client.get(response.headers['Location'])  # Suivi de la redirection
        
        self.assertIn(response.status_code, [200, 404])  # 200 if places exist, 404 if none

    def test_get_place_by_id(self):
        # Success/Fail retrieve a place by its id
        place_id = "place123"
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.check_redirection(response)
        
        if response.status_code == 308:
            response = self.client.get(response.headers['Location'])  # Suivi de la redirection
        
        self.assertIn(response.status_code, [200, 404])  # 200 if exists, 404 if not

    def test_update_place(self):
        # Success/Fail update place information
        place_id = "place123"
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Apartment",
            "description": "A newly renovated place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "amenities": ["wifi", "pool"]
        })
        self.check_redirection(response)
        
        if response.status_code == 308:
            response = self.client.get(response.headers['Location'])  # Suivi de la redirection
        
        self.assertIn(response.status_code, [200, 404])  # 200 if updated, 404 if not found
        
        if response.status_code == 200:
            data = response.get_json()
            self.assertEqual(data['message'], "Place updated successfully")

if __name__ == '__main__':
    unittest.main()
