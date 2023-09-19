from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserLoginView, UserLogoutView

router = DefaultRouter()
router.register(r'api/register', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', UserLoginView.as_view(), name="user-login"),
    path('api/logout/', UserLogoutView.as_view(), name='user-logout'),
]
