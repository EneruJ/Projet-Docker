import unittest
from fastapi.testclient import TestClient
from main import app

# Mise en place des tests unitaires
client = TestClient(app)

class TestApp(unittest.TestCase):
    
    # Test du chemin par défaut, vérification de la réponse reçue
    def test_read_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})
    
    # Test qui vérifie pour un item donné si le résultat affiché est le bon
    def test_read_item(self):
        response = client.get("/items/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"item_id": 1, "q": None})

    # Test de la création d'un Item
    def test_create_item(self):
        data = {
            "name": "Item 1",
            "description": "Description de l'item 1",
            "price": 19.99,
            "is_offer": True
        }
        response = client.post("/items/", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)
    
    def test_read_items(self):
        response = client.get("/items/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
