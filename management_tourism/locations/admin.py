from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Lieu

@admin.register(Lieu)
class LieuAdmin(LeafletGeoAdmin):
    list_display = ('nom', 'description', 'location', 'date_added')
    search_fields = ('nom', 'description')
