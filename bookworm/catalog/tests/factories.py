import factory
from factory.django import DjangoModelFactory

from bookworm.catalog.models import Book, Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    author = factory.Faker("name")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    cover = factory.django.ImageField(color="blue")
    category = factory.SubFactory(CategoryFactory)
