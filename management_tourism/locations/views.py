from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Lieu
from .serializers import LieuSerializer
from django.shortcuts import render


class LieuViewSet(viewsets.ModelViewSet):
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        if lat and lng:
            try:
                user_location = Point(float(lng), float(lat), srid=4326)
                queryset = queryset.annotate(distance=Distance('location', user_location)).order_by('distance')
            except ValueError:
                pass
        return queryset


class MapSearchView(APIView):
    def get(self, request):
        
        # Récupère les paramètres lat, lng, et distance depuis la requête GET
        lat = request.GET.get('lat', 43.610769)
        lng = request.GET.get('lng', 3.876716)
        distance = request.GET.get('distance', 1000)

        if not lat or not lng:
            return Response({'error': 'Les coordonnées sont requises'}, status=400)
        
        # Conversion des paramètres en float
        try:
            lat, lng = float(lat), float(lng)
            distance = float(distance)
        except ValueError:
            return Response({'error': 'Paramètres invalides'}, status=400)
        
        # Crée un point géographique pour l'utilisateur
        user_location = Point(lng, lat, srid=4326)
        
        # Recherche les lieux dans un rayon donné par l'utilisateur et les trie par rayon
        lieux = Lieu.objects.annotate(distance=Distance('location', user_location)) \
                            .filter(distance__lte=distance) \
                            .order_by('distance')

        # Résultats au format GeoJSON
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [lieu.location.x, lieu.location.y]},
                    "properties": {
                        "nom": lieu.nom,
                        "description": lieu.description,
                        "distance": round(lieu.distance.m, 2) if lieu.distance else None
                    }
                } for lieu in lieux
            ]
        }
        return Response(data)

# Vue pour afficher la carte (map.html)
def map_view(request):
    return render(request, 'locations/map.html')

class LieuxListView(APIView):
    def get(self, request):
        lieux = Lieu.objects.all()
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [lieu.location.x, lieu.location.y]},
                    "properties": {"nom": lieu.nom, "description": lieu.description}
                } for lieu in lieux
            ]
        }
        return Response(data)
