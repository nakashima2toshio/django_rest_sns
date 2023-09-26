from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sns_app.views import PostViewSet, LikeViewSet, CommentViewSet, FollowViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
