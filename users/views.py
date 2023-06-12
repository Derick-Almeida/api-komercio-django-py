from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

from utils import IsOwner, IsAdmin
from .serializers import AccountSerializer
from .models import User


class AccountView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = User.objects

    def get_queryset(self):
        if "num" in list(self.kwargs.keys()):
            num_users = self.kwargs["num"]

            return self.queryset.order_by("-date_joined")[0:num_users]

        return self.queryset.all()


class UpdateAccountView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    serializer_class = AccountSerializer
    queryset = User.objects


class ActivateDeactivateAccountView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    serializer_class = AccountSerializer
    queryset = User.objects

    def perform_update(self, serializer):
        serializer.save(is_admin=self.request.user.is_superuser)
