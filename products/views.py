from rest_framework.authentication import TokenAuthentication

from utils.mixins import SerializerByMethodMixin
from .permissions import ProductPermissions
from .permissions import ProductActivePermissions


from rest_framework import generics
from products.models import Product
from . import serializers


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermissions]

    queryset = Product.objects.all()

    serializer_map = {
        "GET": serializers.ProductSerializer,
        "POST": serializers.ProductDetailSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductDetailView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductActivePermissions]

    queryset = Product.objects.all()

    serializer_map = {
        "GET": serializers.ProductDetailSerializer,
        "PATCH": serializers.ProductDetailSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
