from rest_framework.serializers import ModelSerializer

from .models import User


class AccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        )

        read_only_fields = ["date_joined", "is_superuser"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance: User, validated_data: dict) -> User:
        is_admin = validated_data.pop("is_admin", None)

        if is_admin:
            instance.is_active = validated_data.get("is_active", instance.is_active)
            instance.save()
            return instance

        for key, value in validated_data.items():
            if key != "is_active":
                setattr(instance, key, value)

        instance.save()

        return instance
