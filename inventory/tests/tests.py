from unittest import TestCase

from inventory.tests.fixture import (
    InMemoryRepository,
    load_inmemoryrepository_with_existing_products
)
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
                whose='id', equals=some_product_id_that_hasnt_been_added
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

    def test_getproduct_returns_same_product_but_different_object(self):
        product = Product(name='New Product', price=1)
        self.inventory.add(product)
        returned_product = self.inventory.get_product(
            whose='id', equals=product.id
        )
        self.assertNotEqual(id(returned_product), id(product))

    def test_multiple_insertions_at_once(self):
        products = [
            Product(name='test multiple insertions 1', price=1),
            Product(name='test multiple insertions 2', price=2),
            Product(name='test multiple insertions 3', price=3),
        ]
        self.inventory.add_many(products)
        self.assertTrue(
            all(product in self.inventory for product in products)
        )


class InventoryWithExistingProductTest(TestCase):
    def setUp(self):
        repository = load_inmemoryrepository_with_existing_products()
        self.inventory = Inventory(
            repository=repository
        )

    def test_getproduct_returns_existing_product(self):
        expected_product_id = 1
        returned_product = self.inventory.get_product(
            whose='id', equals=expected_product_id
        )
        self.assertEqual(expected_product_id, returned_product.id)

    def test_getproduct_using_name_field_returns_existing_product(self):
        expected_product_id = 1
        returned_product = self.inventory.get_product(
            whose='name', equals='Existing Product'
        )
        self.assertEqual(expected_product_id, returned_product.id)

    def test_exception_raised_if_getproduct_match_more_than_one_product(self):
        with self.assertRaises(LookupError):
            self.inventory.get_product(
                whose='name', equals='Duplicated Product'
            )
