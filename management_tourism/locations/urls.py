from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LieuViewSet, MapSearchView, LieuxListView, map_view

router = DefaultRouter()
router.register(r'lieux', LieuViewSet, basename='lieu')

urlpatterns = [
    path('', map_view, name='home'),
    path('api/', include(router.urls)), 
    path('lieux/search/', LieuViewSet.as_view({'get': 'list'}), name='lieux-search'),
    path('map-search/', MapSearchView.as_view(), name='map-search'),
    path('lieux/', LieuxListView.as_view(), name='lieux-list'),
]
