import pdb
from rest_framework import serializers

from .models import Product
from users.serializers import AccountSerializer


class ProductSerializer(serializers.ModelSerializer):
    seller_id = serializers.UUIDField(source="user.id")

    class Meta:
        model = Product

        fields = (
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(source="user", read_only=True)

    class Meta:
        model = Product

        fields = (
            "id",
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        )

    read_only_fields = ["seller"]

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "the quantity of the product cannot be negative"
            )

        return value
