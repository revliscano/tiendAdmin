from abc import ABC, abstractmethod

from database.sqlalchemy_data_layer import data_access_layer


class RepositoryAdapter(ABC):
    @abstractmethod
    def create(self, record):
        pass

    @abstractmethod
    def get(self, id):
        pass


class SQLAlchemyProductRepository(RepositoryAdapter):
    def create(self, record):
        record_data = record.get_writable_data()
        product_table = data_access_layer.product
        result = data_access_layer.connection.execute(
            product_table.insert(),
            **record_data
        )
        record.id = result.lastrowid

    def get(self, record):
        pass
