from rest_framework import generics

from users.permissions import UserIsAdm, UserIsOwner
from .models import User
from .serializers import UserManagementSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        num = self.kwargs["date_joined"]
        return self.queryset.order_by("date_joined")[0:num]


class UserUpdateView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserIsOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserManagementView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserIsAdm]

    queryset = User.objects.all()
    serializer_class = UserManagementSerializer
