from rest_framework import serializers

from users.serializers import UserSerializer
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    seller_id = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Product
        fields = ["seller_id", "description", "price", "quantity", "is_active"]
        read_only_fields = ["is_active", "seller_id"]
        depth = 0


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "seller", "description", "price", "quantity", "is_active"]
        read_only_fields = ["id", "is_active", "seller"]
        depth = 1
