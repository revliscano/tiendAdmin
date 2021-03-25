from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):
    @abstractmethod
    def add_record(self, record):
        pass

    @abstractmethod
    def get_record(self, id):
        pass


class Product:
    def __init__(self, name, price):
        self.id = None
        self.name = name
        self.price = price

    def get_data(self):
        return self.id, self.name, self.price

    def __eq__(self, another_product):
        return self.id == another_product.id


class Inventory:
    def __init__(self, database_adapter):
        self.db = database_adapter

    def add(self, product):
        self.db.add_record(product)

    def get_product(self, id_):
        return self.db.get_record(id_, Product)

    def __contains__(self, product):
        try:
            return self.get_product(product.id) is not None
        except ValueError:
            return False
