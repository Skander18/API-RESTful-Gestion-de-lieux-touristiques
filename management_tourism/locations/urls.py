
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import map_view
from .views import LieuViewSet


router = DefaultRouter()
router.register(r'lieux', LieuViewSet, basename='lieu')

urlpatterns = [
    path('', include(router.urls)),
    path('lieux/search/', LieuViewSet.as_view({'get': 'list'}), name='lieux-search'),
    path('map/', map_view, name='map'),
]