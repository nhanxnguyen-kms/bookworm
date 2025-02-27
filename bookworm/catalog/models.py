from typing import ClassVar

from django.db import models

from bookworm.catalog.validations import validate_cover_image


class Book(models.Model):
    """
    Model representing a book.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(
        upload_to="covers/", blank=True, validators=[validate_cover_image]
    )
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)

    objects: ClassVar[models.Manager] = models.Manager()

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Model representing a book category.
    """

    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=200)

    objects: ClassVar[models.Manager] = models.Manager()

    def __str__(self):
        return self.name
