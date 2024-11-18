import requests
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.db import transaction
from locations.models import Lieu


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        url = "http://overpass-api.de/api/interpreter"
        query = '''
        [out:json];
        area[name="Montpellier"]->.searchArea;
        (node["cuisine"="pizza"](area.searchArea););
        out;
        '''
        try:
            response = requests.get(url, params={'data': query}, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.import_data(data)
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de la récupération des données : {e}"))

    @transaction.atomic
    def import_data(self, data):
        lieux_to_create = []
        for element in data.get('elements', []):
            if element['type'] == 'node':
                nom = element.get('tags', {}).get('name', 'Inconnu')
                description = element.get('tags', {}).get('cuisine', 'Pizza')
                lat, lng = element['lat'], element['lon']
                location = Point(lng, lat, srid=4326)

                if not Lieu.objects.filter(location=location).exists():
                    lieux_to_create.append(Lieu(nom=nom, description=description, location=location))

        Lieu.objects.bulk_create(lieux_to_create)
        self.stdout.write(self.style.SUCCESS(f"{len(lieux_to_create)} lieux ajoutés avec succès."))
