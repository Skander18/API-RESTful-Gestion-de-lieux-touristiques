from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework import viewsets
from .models import Lieu
from .serializers import LieuSerializer
# Create your views here.


def map_search(request):
    # Extraire les paramètres de la requête
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    distance = request.GET.get('distance')

    if not lat or not lng:
        return JsonResponse({'error': 'Les coordonnées sont requises'}, status=400)

    # Convertir les paramètres en flottants
    lat = float(lat)
    lng = float(lng)
    distance = float(distance) if distance else 1000  # distance à 1000 mètres

    user_location = Point(lng, lat, srid=4326)
    
    # Filtrer les lieux par distance et trier par proximité
    lieux = Lieu.objects.annotate(distance=Distance('location', user_location)) \
                        .filter(distance__lte=distance) \
                        .order_by('distance')

    # Réponse en GeoJSON
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lieu.location.x, lieu.location.y]
                },
                "properties": {
                    "nom": lieu.nom,
                    "description": lieu.description,
                    "distance": round(lieu.distance.m) if lieu.distance else None
                }
            }
            for lieu in lieux
        ]
    }
    return JsonResponse(data)


def lieux_list(request):
    lieux = Lieu.objects.all()
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lieu.location.x, lieu.location.y]
                },
                "properties": {
                    "nom": lieu.nom,
                    "description": lieu.description
                }
            }
            for lieu in lieux
        ]
    }
    return JsonResponse(data)

def map_view(request):
    return render(request, 'locations/map.html')


class LieuViewSet(viewsets.ModelViewSet):
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer
    
    def get_queryset(self):
            queryset = Lieu.objects.all()
            lat = self.request.query_params.get('lat')
            lng = self.request.query_params.get('lng')
            if lat and lng:
                try:
                    user_location = Point(float(lng), float(lat), srid=4326)
                    queryset = queryset.annotate(distance=Distance('location', user_location)).order_by('distance')
                except ValueError:
                    pass
            return queryset



