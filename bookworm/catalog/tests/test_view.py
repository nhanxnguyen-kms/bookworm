from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from bookworm.catalog.models import Book, Category
from bookworm.catalog.tests.factories import BookFactory, CategoryFactory


class BookViewSetTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.book = BookFactory(category=self.category)

    def tearDown(self):
        self.book.cover.delete()

    def test_list_books(self):
        response = self.client.get(reverse("books-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book.title)

    def test_retrieve_book(self):
        response = self.client.get(reverse("books-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_create_book(self):
        with open(self.book.cover.path, "rb") as cover_file:
            data = {
                "title": "New Book",
                "description": "A description of the new book",
                "author": "Author Name",
                "price": "19.99",
                "cover": cover_file,
                "category": self.category.id,
            }
            response = self.client.post(reverse("books-list"), data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=response.data["id"]).title, "New Book")

    def test_update_book(self):
        with open(self.book.cover.path, "rb") as cover_file:
            data = {
                "title": "Updated Book",
                "description": self.book.description,
                "author": self.book.author,
                "price": str(self.book.price),
                "cover": cover_file,
                "category": self.category.id,
            }
            response = self.client.put(
                reverse("books-detail", args=[self.book.id]), data, format="multipart"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(reverse("books-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()

    def test_list_categories(self):
        response = self.client.get(reverse("categories-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.category.name)

    def test_retrieve_category(self):
        response = self.client.get(
            reverse("categories-detail", args=[self.category.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)

    def test_create_category(self):
        data = {"name": "New Category"}
        response = self.client.post(reverse("categories-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(
            Category.objects.get(id=response.data["id"]).name, "New Category"
        )

    def test_update_category(self):
        data = {"name": "Updated Category"}
        response = self.client.put(
            reverse("categories-detail", args=[self.category.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Category")

    def test_delete_category(self):
        response = self.client.delete(
            reverse("categories-detail", args=[self.category.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
