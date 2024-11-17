from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.gis.geos import Point
from locations.models import Lieu

class LieuAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Prépare les données partagées pour tous les tests (exécutée une seule fois).
        """
        cls.client = APIClient()

        # Création des lieux de test
        cls.lieu1 = Lieu.objects.create(
            nom="Il Pizzaiolo 1", description="pizza",
            location=Point(3.8758721, 43.6109756)
        )
        cls.lieu2 = Lieu.objects.create(
            nom="Nouvelle Pizza", description="pizza",
            location=Point(3.8826072, 43.6039274)
        )
        cls.lieu3 = Lieu.objects.create(
            nom="Domino's Pizza", description="pizza",
            location=Point(3.8769586, 43.6156869)
        )
        cls.lieux_url = reverse('lieu-list')
        cls.search_url = reverse('lieux-search')

    def test_create_lieu(self):
        """
        Teste la création d'un nouveau lieu via l'API.
        """
        data = {
            "nom": "Pizza Hut",
            "description": "Chaîne de pizza",
            "location": {"type": "Point", "coordinates": [3.877540, 43.612850]}
        }
        response = self.client.post(self.lieux_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lieu.objects.count(), 4)

    def test_get_lieu_list(self):
        """Vérifie que l'API retourne tous les lieux existants."""
        response = self.client.get(self.lieux_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_search_nearby_lieux(self):
        """Test de la recherche géospatiale."""
        response = self.client.get(
            f"{self.search_url}?lat=43.6109756&lng=3.8758721&distance=1000"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lieux = response.data['features']
        self.assertGreater(len(lieux), 0)

        # Vérifie que chaque lieu a une distance valide
        self.assertTrue(all(
            lieu['properties'].get('distance') <= 1000 for lieu in lieux
        ))

    def test_update_lieu(self):
        """Test de mise à jour d'un lieu existant."""
        url = reverse('lieu-detail', args=[self.lieu1.id])
        updated_data = {
            "nom": "Il Pizzaiolo 1 - Mise à jour",
            "description": "Pizzeria mise à jour",
            "location": {"type": "Point", "coordinates": [3.8758721, 43.6109756]}
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifie que la mise à jour est bien effectuée
        self.lieu1.refresh_from_db()
        self.assertEqual(self.lieu1.nom, "Il Pizzaiolo 1 - Mise à jour")

    def test_delete_lieu(self):
        """Test de suppression d'un lieu."""
        response = self.client.delete(reverse('lieu-detail', args=[self.lieu2.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lieu.objects.count(), 2)

    def test_search_with_invalid_coordinates(self):
        """Vérifie le comportement avec des coordonnées invalides."""
        response = self.client.get(f"{self.search_url}?lat=invalid&lng=invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
