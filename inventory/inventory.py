from abc import ABC, abstractmethod


class RepositoryAdapter(ABC):
    @abstractmethod
    def create(self, record):
        pass

    @abstractmethod
    def get(self, id):
        pass


class Product:
    def __init__(self, name, price, id_=None):
        self.id = id_
        self.name = name
        self.price = price

    def get_data(self):
        return self.id, self.name, self.price

    def __eq__(self, another_product):
        return self.id == another_product.id


class Inventory:
    def __init__(self, repository):
        self.repository = repository

    def add(self, product):
        if product.id is not None:
            raise ValueError("Product can't have an already assigned id")
        self.repository.create(product)

    def get_product(self, id_):
        record = self.repository.get(id_)
        object_id, *rest_of_data = record
        product = Product(*rest_of_data, id_=object_id)
        return product

    def __contains__(self, product):
        try:
            return self.get_product(product.id) is not None
        except LookupError:
            return False
