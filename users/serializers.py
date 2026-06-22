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


class UserSerializer(serializers.ModelSerializer):
    is_super_admin = serializers.SerializerMethodField()
    is_manager = serializers.SerializerMethodField()

    class Meta:
        model = user_model
        fields = ("id", "username", "email", "is_super_admin", "is_manager")

    def get_is_super_admin(self, obj):
        return obj.is_superuser or obj.groups.filter(name="SUPER_ADMIN").exists()

    def get_is_manager(self, obj):
        return obj.groups.filter(name="MANAGER").exists()
