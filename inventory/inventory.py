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


class Product:
    def __init__(self, name, price, id_=None):
        self.id = id_
        self.name = name
        self.price = price

    def get_data(self):
        return dict(self.__dict__)

    def get_writable_data(self):
        data = dict(self.__dict__)
        data.pop('id')
        return data

    def get_data_values(self):
        return self.__dict__.values()

    def __eq__(self, another_product):
        return self.id == another_product.id
