import requests
from django.core.management.base import BaseCommand
from locations.models import Lieu
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Importe des lieux depuis OpenStreetMap (exemple : pizzerias en Montpellier)'

    def handle(self, *args, **kwargs):
        url = "http://overpass-api.de/api/interpreter"
        query = '''
        [out:json];
        area[name="Montpellier"]->.searchArea;
        (node["cuisine"="pizza"](area.searchArea););
        out;
        '''

        response = requests.get(url, params={'data': query})

        if response.status_code == 200:
            data = response.json()
            self.import_data(data)
        else:
            self.stdout.write(self.style.ERROR(f"Erreur lors de la récupération des données : {response.status_code}"))

    def import_data(self, data):
        count = 0
        for element in data['elements']:
            if element['type'] == 'node':
                nom = element.get('tags', {}).get('name', 'Inconnu')
                description = element.get('tags', {}).get('cuisine', 'Pizza')
                lat = element['lat']
                lng = element['lon']
                location = Point(lng, lat)

                # Vérifier si le lieu existe déjà pour éviter les doublons
                if not Lieu.objects.filter(location=location).exists():
                    Lieu.objects.create(
                        nom=nom,
                        description=description,
                        location=location
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"Importation terminée avec succès. {count} lieux ajoutés."))
