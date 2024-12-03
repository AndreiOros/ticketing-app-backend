from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginAPIView, ChangePasswordView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('organisation/', LoginAPIView.as_view(), name='login'),
]
