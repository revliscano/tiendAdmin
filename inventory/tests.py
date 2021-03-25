from unittest import TestCase
from inventory.models import Product, Inventory, DatabaseAdapter


class InventoryTest(TestCase):
    def setUp(self):
        self.product = Product(name='foo', price=100)
        self.inventory = Inventory(database_adapter=MockDB())

    def test_adds_product(self):
        self.inventory.add(self.product)
        self.assertTrue(self.product in self.inventory)

    def test_exception_raised_when_attempt_to_add_product_with_id(self):
        self.product.id = 1
        with self.assertRaises(ValueError):
            self.inventory.add(self.product)

    def test_containment_checks_for_product_id(self):
        product_with_identical_data = Product(name='foo', price=100)
        self.inventory.add(self.product)
        self.assertFalse(product_with_identical_data in self.inventory)


class InventoryWithExistingProductTest(TestCase):
    def setUp(self):
        self.product = Product(name='foo', price=100)
        database_with_existing_product = MockDB()
        database_with_existing_product.add_record(self.product)
        self.inventory = Inventory(
            database_adapter=database_with_existing_product
        )

    def test_get_product_returns_existing_product(self):
        returned_product = self.inventory.get_product(id_=self.product.id)
        self.assertEqual(returned_product, self.product)

    def test_get_product_returns_same_product_but_different_object(self):
        returned_product = self.inventory.get_product(id_=self.product.id)
        self.assertNotEqual(id(returned_product), id(self.product))


class MockDB(DatabaseAdapter):
    LAST_PRODUCT = -1
    ID = 0

    def __init__(self):
        self.records = []

    def add_record(self, object_):
        last_id = (
            self.records[self.LAST_PRODUCT].id
            if self.records
            else 0
        )
        object_.id = last_id + 1
        self.records.append(object_.get_data())

    def get_record(self, id_):
        try:
            return next(
                stored_object
                for stored_object in self.records
                if stored_object[self.ID] == id_
            )
        except StopIteration:
            raise ValueError('Object not in inventory')
