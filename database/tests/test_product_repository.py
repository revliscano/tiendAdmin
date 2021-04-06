from unittest import TestCase, skip

from inventory.inventory import Product
from database.repository import SQLAlchemyProductRepository
from database.sqlalchemy_data_layer import data_access_layer
from database.tests.fixture import populate_database_with_products


class SQLAlchemyProductRepositoryTest(TestCase):
    @classmethod
    def setUpClass(class_):
        data_access_layer.db_init('sqlite:///:memory:')
        populate_database_with_products()

    def setUp(self):
        self.repository = SQLAlchemyProductRepository()

    def test_create_method_assigns_an_id_to_product(self):
        product = Product(name='foo', price=1)
        self.repository.create(record=product)
        self.assertIsNotNone(product.id)

    def test_get_method_returns_expected_product_data(self):
        expected_product_name, expected_product_price = 'Some Product', 1000
        product_data = self.repository.get(field_name='id', value=1)
        self.assertIn(expected_product_name, product_data)
        self.assertIn(expected_product_price, product_data)

    def test_get_method_returns_expected_product_data_when_passed_name(self):
        expected_product_name, expected_product_price = 'Some Product', 1000
        product_data = self.repository.get(
            field_name='name',
            value=expected_product_name
        )
        self.assertIn(expected_product_name, product_data)
        self.assertIn(expected_product_price, product_data)

    @classmethod
    def tearDownClass(class_):
        data_access_layer.close_connection()
