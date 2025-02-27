from rest_framework.test import APITestCase

from bookworm.catalog.api.serializers import BookSerializer, CategorySerializer
from bookworm.catalog.tests.factories import BookFactory, CategoryFactory


class CategorySerializerTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.serializer = CategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["id", "name"])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.category.name)


class BookSerializerTest(APITestCase):
    def setUp(self):
        self.book = BookFactory()
        self.serializer = BookSerializer(instance=self.book)

    def tearDown(self):
        self.book.cover.delete()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ["id", "title", "description", "author", "price", "cover", "category"],
        )

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["title"], self.book.title)

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["description"], self.book.description)

    def test_author_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["author"], self.book.author)

    def test_price_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["price"], str(self.book.price))

    def test_cover_field_content(self):
        data = self.serializer.data
        self.assertTrue("cover" in data)

    def test_category_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["category"], self.book.category.id)
