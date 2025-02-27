from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookworm.user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Serializes the id, email, name, and username fields of the User model.
    """

    class Meta:
        model = User
        fields = ("id", "email", "name", "username")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
