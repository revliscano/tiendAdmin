from unittest import TestCase
from inventory.models import Product, Inventory, DatabaseAdapter


class MockDB(DatabaseAdapter):
    LAST_PRODUCT = -1

    def __init__(self):
        self.records = []

    def add_record(self, object_):
        last_id = self.records[self.LAST_PRODUCT].id if self.records else 0
        object_.id = last_id + 1
        self.records.append(object_)

    def get_record(self, id_, model_class):
        try:
            object_ = next(
                stored_object
                for stored_object in self.records
                if stored_object.id == id_
            )
            object_id, *rest_of_data = object_.get_data()
            new_object = model_class(*rest_of_data)
            new_object.id = object_id
            return new_object
        except StopIteration:
            raise ValueError('Object not in inventory')


class TestInventory(TestCase):
    def setUp(self):
        self.product = Product(name='foo', price=100)
        self.inventory = Inventory(database_adapter=MockDB())

    def test_adds_product(self):
        self.inventory.add(self.product)
        self.assertTrue(self.product in self.inventory)

    def test_containment_checks_for_product_id(self):
        product_with_identical_data = Product(name='foo', price=100)
        self.inventory.add(self.product)
        self.assertFalse(product_with_identical_data in self.inventory)

    def test_returns_product(self):
        self.inventory.add(self.product)
        returned_product = self.inventory.get_product(id_=self.product.id)
        self.assertEqual(returned_product, self.product)

    def test_get_returns_a_fresh_new_product(self):
        self.inventory.add(self.product)
        returned_product = self.inventory.get_product(id_=self.product.id)
        self.assertNotEqual(id(returned_product), id(self.product))
