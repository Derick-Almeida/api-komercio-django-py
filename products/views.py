from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

from utils import (
    IsSellerOrReadOnly,
    IsSellerAndOwnerOrReadOnly,
    SerializerByMethodMixin,
)
from .serializers import ProductSerializer, ProductDetailSerializer
from .models import Product


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerAndOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
