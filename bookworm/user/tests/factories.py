import factory
from factory.django import DjangoModelFactory

from bookworm.user.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    name = factory.Faker("name")
    password = factory.Faker("password")
    is_staff = factory.Faker("boolean")
    is_active = factory.Faker("boolean")
