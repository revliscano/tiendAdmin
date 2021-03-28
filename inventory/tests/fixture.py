from inventory.inventory import RepositoryAdapter


class InMemoryRepository(RepositoryAdapter):
    LAST_PRODUCT = -1
    ID = 0

    def __init__(self):
        self.records = []

    def create(self, object_):
        last_id = (
            self.records[self.LAST_PRODUCT].id
            if self.records
            else 0
        )
        object_.id = last_id + 1
        self.records.append(object_.get_data())

    def get(self, id_):
        try:
            return next(
                stored_object
                for stored_object in self.records
                if stored_object[self.ID] == id_
            )
        except StopIteration:
            raise LookupError('Object not in inventory')
