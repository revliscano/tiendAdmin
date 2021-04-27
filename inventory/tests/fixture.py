from database.repository import RepositoryAdapter


LAST_PRODUCT = -1


def load_inmemoryrepository_with_existing_products():
    repository = InMemoryRepository()
    repository.create({'name': 'Existing Product', 'price': 100})
    repository.create({'name': 'Duplicated Product', 'price': 200})
    repository.create({'name': 'Duplicated Product', 'price': 200})
    return repository


class InMemoryRepository(RepositoryAdapter):

    def __init__(self):
        self.records = []

    def create(self, data):
        last_id = (
            self.records[LAST_PRODUCT]['id']
            if self.records
            else 0
        )
        record = dict(id=last_id + 1, **data)
        self.records.append(record)
        return record['id']

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

    def bulk_create(self, records):
        return [self.create(record) for record in records]
