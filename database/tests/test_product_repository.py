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

    def tearDown(self):
        clear_table()


class BulkCreateTest(SQLAlchemyProductRepositoryTest):
    def setUp(self):
        super().setUp()
        self.records = [
            {'name': 'test multiple insertions 1', 'price': 100},
            {'name': 'test multiple insertions 2', 'price': 200},
            {'name': 'test multiple insertions 3', 'price': 300},
            {'name': 'test multiple insertions 4', 'price': 400},
            {'name': 'test multiple insertions 5', 'price': 500},
            {'name': 'test multiple insertions 6', 'price': 600},
        ]

    def test_returns_expected_ids(self):
        first_batch_ids = self.repository.bulk_create(self.records[:3])
        second_batch_ids = self.repository.bulk_create(self.records[3:])
        self.assertEqual((1, 2, 3), first_batch_ids)
        self.assertEqual((4, 5, 6), second_batch_ids)

    def test_get_expected_record_after_bulkcreate(self):
        ids = self.repository.bulk_create(self.records)
        returned_record_whose_id_should_be_1 = self.repository.get(
            field_name='id', value=ids[0]
        )
        returned_record_whose_id_should_be_5 = self.repository.get(
            field_name='id', value=ids[4]
        )
        self.assertIn(
            'test multiple insertions 1', returned_record_whose_id_should_be_1
        )
        self.assertIn(
            'test multiple insertions 5', returned_record_whose_id_should_be_5
        )


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
