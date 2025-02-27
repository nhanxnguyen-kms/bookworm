from rest_framework import serializers

from bookworm.catalog.models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Serializes all fields of the Category model.
    """

    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Serializes all fields of the Book model.
    """

    class Meta:
        model = Book
        fields = "__all__"
