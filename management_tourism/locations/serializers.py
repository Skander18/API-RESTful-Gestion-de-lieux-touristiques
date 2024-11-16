from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Lieu

class LieuSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Lieu
        fields = ['id', 'nom', 'description', 'location', 'date_added']
        geo_field = 'location'