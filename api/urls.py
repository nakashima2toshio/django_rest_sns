from django.middleware import csrf
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from api.views import CustomUserViewSet, ProfileViewSet
from api.views import LogoutView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('csrf/', csrf, name='csrf'),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

#  path('myself/', ManageUserView.as_view(), name='myself'),

