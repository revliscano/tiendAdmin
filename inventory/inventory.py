class Inventory:
    def __init__(self, repository):
        self.repository = repository

    def add(self, product):
        if product.has_id():
            raise ValueError("Product can't have an already assigned id")
        product_data = product.get_writable_data()
        assigned_id = self.repository.create(product_data)
        product.id = assigned_id

    def add_many(self, products):
        products_data = [product.get_writable_data() for product in products]
        ids = self.repository.bulk_create(products_data)
        for id_, product in zip(ids, products):
            product.id = id_

    def get_product(self, which, equals):
        record = self.repository.get(which, equals)
        object_id, *rest_of_data = record
        product = Product(*rest_of_data, id_=object_id)
        return product

    def __contains__(self, product):
        try:
            return self.get_product(
                which='id', equals=product.id
            ) is not None
        except LookupError:
            return False


class Product:
    def __init__(self,
                 name,
                 price,
                 quantity=0,
                 is_fixed_to_USD=True,
                 id_=None):
        self.id = id_
        self.name = name
        self.price = price
        self.quantity = quantity
        self.is_fixed_to_USD = is_fixed_to_USD

    def has_id(self):
        return self.id is not None

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
