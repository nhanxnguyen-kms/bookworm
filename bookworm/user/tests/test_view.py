from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from bookworm.user.models import User
from bookworm.user.tests.factories import UserFactory


class UserViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], self.user.username)

    def test_retrieve_user(self):
        response = self.client.get(reverse("users-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_create_user(self):
        data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(reverse("users-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=response.data["id"]).name, "New User")

    def test_update_user(self):
        data = {
            "name": "Updated User",
            "email": self.user.email,
            "password": "updatedpassword123",
        }
        response = self.client.put(reverse("users-detail", args=[self.user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Updated User")

    def test_delete_user(self):
        response = self.client.delete(reverse("users-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
