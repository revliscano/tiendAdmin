from abc import ABC, abstractmethod

from database.sqlalchemy_data_layer import data_access_layer


class RepositoryAdapter(ABC):
    @abstractmethod
    def create(self, record):
        pass

    @abstractmethod
    def get(self, id_):
        pass


class SQLAlchemyProductRepository(RepositoryAdapter):

    table = data_access_layer.product

    def create(self, record):
        record_data = record.get_writable_data()
        result = data_access_layer.connection.execute(
            self.table.insert(),
            **record_data
        )
        record.id = result.lastrowid

    def get(self, id_):
        self.table = data_access_layer.product
        product = data_access_layer.connection.execute(
            self.table.select().where(self.table.columns.id == id_)
        ).first()
        if not product:
            raise LookupError('Object not in inventory')
        return product._mapping.values()
