from database.repository import RepositoryAdapter


LAST_PRODUCT = -1


class InMemoryRepository(RepositoryAdapter):

    def __init__(self):
        self.records = []

    def create(self, object_):
        last_id = (
            self.records[LAST_PRODUCT].id
            if self.records
            else 0
        )
        object_.id = last_id + 1
        self.records.append(
            object_.get_data()
        )

    def get(self, field_name, value):
        try:
            record_data = next(
                record
                for record in self.records
                if record[field_name] == value
            )
            return record_data.values()
        except StopIteration:
            raise LookupError('Object not in inventory')
