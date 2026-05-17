from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import User

user_model = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    class Meta:
        model = user_model
        fields = ('id','username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user