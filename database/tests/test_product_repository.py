from unittest import TestCase

from database.repository import SQLAlchemyProductRepository
from database.sqlalchemy_data_layer import data_access_layer
from database.tests.fixture import (
    populate_database_with_products, clear_table
)


class SQLAlchemyProductRepositoryTest(TestCase):

    @classmethod
    def setUpClass(class_):
        data_access_layer.db_init('sqlite:///:memory:')
        clear_table()

    def setUp(self):
        self.repository = SQLAlchemyProductRepository()

    def test_create_method_returns_id(self):
        product_data = {'name': 'foo', 'price': 1}
        id_ = self.repository.create(record=product_data)
        self.assertEqual(1, id_)

    def test_bulkcreate_method_returns_ids(self):
        records = [
            {'name': 'test multiple insertions 1', 'price': 1},
            {'name': 'test multiple insertions 2', 'price': 2},
            {'name': 'test multiple insertions 3', 'price': 3},
        ]
        ids = self.repository.bulk_create(records)
        self.assertEqual((1, 2, 3), ids)

    def tearDown(self):
        clear_table()


class SQLAlchemyProductRepositoryWithPopulatedDBTest(TestCase):

    @classmethod
    def setUpClass(class_):
        data_access_layer.db_init('sqlite:///:memory:')
        populate_database_with_products()

    def setUp(self):
        self.repository = SQLAlchemyProductRepository()

    def test_get_method_returns_expected_product_data(self):
        expected_product_name, expected_product_price = 'Existing Product', 100
        product_data = self.repository.get(field_name='id', value=1)
        self.assertIn(expected_product_name, product_data)
        self.assertIn(expected_product_price, product_data)

    def test_get_method_returns_expected_product_data_when_passed_name(self):
        expected_product_name, expected_product_price = 'Existing Product', 100
        product_data = self.repository.get(
            field_name='name',
            value=expected_product_name
        )
        self.assertIn(expected_product_name, product_data)
        self.assertIn(expected_product_price, product_data)

    def test_get_method_raises_exception_if_finds_more_than_one_row(self):
        with self.assertRaises(LookupError):
            self.repository.get(
                field_name='name',
                value='Duplicated Product'
            )
