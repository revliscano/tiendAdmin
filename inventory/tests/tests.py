from unittest import TestCase

from inventory.tests.fixture import InMemoryRepository
from inventory.inventory import Product, Inventory


class InventoryTest(TestCase):
    def setUp(self):
        self.product = Product(name='foo', price=100)
        self.inventory = Inventory(repository=InMemoryRepository())

    def test_adds_product(self):
        self.inventory.add(self.product)
        self.assertTrue(self.product in self.inventory)

    def test_exception_raised_when_product_not_found(self):
        some_product_id_that_hasnt_been_added = 9999
        with self.assertRaises(LookupError):
            self.inventory.get_product(
                id_=some_product_id_that_hasnt_been_added
            )

    def test_exception_raised_when_attempt_to_add_product_with_id(self):
        self.product.id = 1
        with self.assertRaises(ValueError):
            self.inventory.add(self.product)

    def test_containment_checks_for_product_id(self):
        product_with_identical_data_but_different_id = Product(
            name='foo', price=100
        )
        self.inventory.add(self.product)
        self.assertFalse(
            product_with_identical_data_but_different_id in self.inventory
        )


class InventoryWithExistingProductTest(TestCase):
    def setUp(self):
        product = Product(name='foo', price=100)
        repository_with_existing_product = InMemoryRepository()
        repository_with_existing_product.create(product)
        self.inventory = Inventory(
            repository=repository_with_existing_product
        )

    def test_get_product_returns_existing_product(self):
        expected_product = Product(name='foo', price=100)
        expected_product_id = 1
        expected_product.id = expected_product_id
        returned_product = self.inventory.get_product(id_=expected_product_id)
        self.assertEqual(returned_product, expected_product)

    def test_get_product_returns_same_product_but_different_object(self):
        expected_product = Product(name='foo', price=100)
        expected_product_id = 1
        expected_product.id = expected_product_id
        returned_product = self.inventory.get_product(id_=expected_product_id)
        self.assertNotEqual(id(returned_product), id(expected_product))
