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

    def get(self, field_name, value):
        field = getattr(self.table.columns, field_name)
        result = data_access_layer.connection.execute(
            self.table.select().where(field == value)
        ).fetchmany(2)
        self._validate_fetched(result)
        return result[0]._mapping.values()

    def _validate_fetched(self, result):
        if not result:
            raise LookupError('Object not in inventory')
        if len(result) > 1:
            raise LookupError(
                'There is more than one object '
                'matching given criteria'
            )
