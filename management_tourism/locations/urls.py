
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import lieux_list, map_view, map_search
from .views import LieuViewSet


router = DefaultRouter()
router.register(r'lieux', LieuViewSet, basename='lieu')

urlpatterns = [
    path('', include(router.urls)),
    path('lieux/search/', LieuViewSet.as_view({'get': 'list'}), name='lieux-search'),
    path('map-search/', map_search, name='map-search'),
    path('lieux/', lieux_list, name='lieux-list'),
    path('map/', map_view, name='map'),
]