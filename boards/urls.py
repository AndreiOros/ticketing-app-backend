from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListViewSet, CardViewSet, BoardViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'lists', ListViewSet, basename='list')
router.register(r'cards', CardViewSet, basename='card')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]