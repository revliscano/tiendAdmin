from database.repository import RepositoryAdapter
from inventory.inventory import Product


LAST_PRODUCT = -1


def load_repository_with_existing_products():
    repository = InMemoryRepository()
    repository.create(Product(name='Existing Product', price=100))
    repository.create(Product(name='Duplicated Product', price=200))
    repository.create(Product(name='Duplicated Product', price=200))
    return repository


class InMemoryRepository(RepositoryAdapter):

    def __init__(self):
        self.records = []

    def create(self, object_):
        last_id = (
            self.records[LAST_PRODUCT]['id']
            if self.records
            else 0
        )
        object_.id = last_id + 1
        self.records.append(
            object_.get_data()
        )

    def get(self, field_name, value):
        try:
            matching_records = (
                record
                for record in self.records
                if record[field_name] == value
            )
            record_data = next(matching_records).values()
            if next(matching_records, False):
                raise LookupError(
                    'There is more than one object '
                    'matching given criteria'
                )
            return record_data
        except StopIteration:
            raise LookupError('Object not in inventory')
