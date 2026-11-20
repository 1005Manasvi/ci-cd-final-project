"""Unit tests for product model operations."""

from unittest import TestCase

from service.models import Product
from tests.factories import fake_products


class ProductModelTest(TestCase):
    """Product model CRUD and finder tests."""

    def setUp(self):
        Product.clear()
        self.products = [
            Product.create(**attributes) for attributes in fake_products()
        ]

    def tearDown(self):
        Product.clear()

    def test_read_product(self):
        product = Product.find(self.products[0].id)
        self.assertEqual(product.name, "Coffee Maker")

    def test_update_product(self):
        product = Product.update(self.products[0].id, price=39.99)
        self.assertEqual(product.price, 39.99)

    def test_delete_product(self):
        self.assertTrue(Product.delete(self.products[0].id))
        self.assertIsNone(Product.find(self.products[0].id))

    def test_list_all_products(self):
        self.assertEqual(len(Product.all()), 3)

    def test_find_by_name(self):
        found = Product.find_by_name("coffee")
        self.assertEqual([product.name for product in found], ["Coffee Maker"])

    def test_find_by_category(self):
        found = Product.find_by_category("kitchen")
        self.assertEqual([product.name for product in found], ["Coffee Maker"])

    def test_find_by_availability(self):
        found = Product.find_by_availability(False)
        self.assertEqual([product.name for product in found], ["Desk Lamp"])
