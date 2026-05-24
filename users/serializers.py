from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.services import user_service

user_model = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = user_model
        fields = ("id", "username", "last_name", "email", "password")

    def create(self, validated_data):
        return user_service.create_user(
            username=validated_data["username"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
