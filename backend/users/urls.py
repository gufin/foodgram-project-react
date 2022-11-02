from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .token_views import CustomAuthToken, DestroyTokenAPIView
from .views import UserViewSet

router = DefaultRouter()

router.register('', UserViewSet, basename='users')

auth_urlpatterns = [
    path('login/', CustomAuthToken.as_view()),
    path('logout/', DestroyTokenAPIView.as_view()),
]

urlpatterns = [
    path('auth/token/', include(auth_urlpatterns)),
    path('users/', include(router.urls))
]
