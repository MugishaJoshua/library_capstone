from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from .views import RegisterUser
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterUser.as_view(), name='register'),
    path('auth/login/', obtain_auth_token, name='login'),
]
