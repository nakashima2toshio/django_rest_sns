#
from requests import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from api.models import CustomUser
from api.serializers import CustomUserSerializer, ProfileSerializer
from sns_app.models import Profile as SnsProfile


class LogoutView(APIView):
    @staticmethod
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CustomUser.objects.filter(id=user.id)
        return CustomUser.objects.none()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = SnsProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return SnsProfile.objects.filter(custom_user=user)
        return SnsProfile.objects.none()
