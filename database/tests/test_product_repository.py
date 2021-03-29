from unittest import TestCase

from inventory.inventory import Product
from database.repository import SQLAlchemyProductRepository
from database.sqlalchemy_data_layer import data_access_layer


class SQLAlchemyProductRepositoryTest(TestCase):
    @classmethod
    def setUpClass(cls):
        data_access_layer.db_init('sqlite:///:memory:')

    def test_create_method_assigns_an_id_to_product(self):
        product = Product(name='foo', price=1)
        repository = SQLAlchemyProductRepository()
        repository.create(record=product)
        self.assertIsNotNone(product.id)
