from unittest import TestCase

from inventory.inventory import Product
from database.repository import SQLAlchemyProductRepository
from database.sqlalchemy_data_layer import data_access_layer
from database.tests.fixture import populate_database_with_products


class SQLAlchemyProductRepositoryTest(TestCase):
    @classmethod
    def setUpClass(class_):
        data_access_layer.db_init('sqlite:///:memory:')
        populate_database_with_products()

    def test_create_method_assigns_an_id_to_product(self):
        product = Product(name='foo', price=1)
        repository = SQLAlchemyProductRepository()
        repository.create(record=product)
        self.assertIsNotNone(product.id)

    def test_get_method_returns_expected_product_data(self):
        expected_product_name = 'Some Product'
        expected_product_price = 1000
        repository = SQLAlchemyProductRepository()
        product_data = repository.get(id_=1)
        self.assertIn(expected_product_name, product_data)
        self.assertIn(expected_product_price, product_data)

    @classmethod
    def tearDownClass(class_):
        # data_access_layer.close_connection()
        pass
