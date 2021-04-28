class Inventory:
    def __init__(self, repository):
        self.repository = repository

    def add(self, product):
        product.validate_no_id()
        assigned_id = self.repository.create(product.data)
        product.id = assigned_id

    def add_many(self, products):
        products_data = self._get_data_of(products)
        ids = self.repository.bulk_create(products_data)
        self._assign_ids(products, ids)

    def _get_data_of(self, products):
        products_data = []
        for product in products:
            product.validate_no_id()
            products_data.append(product.data)
        return products_data

    def _assign_ids(self, products, ids):
        for id_, product in zip(ids, products):
            product.id = id_

    def get_product(self, whose, equals):
        record = self.repository.get(whose, equals)
        object_id, *rest_of_data = record
        product = Product(*rest_of_data, id_=object_id)
        return product

    def __contains__(self, product):
        try:
            return self.get_product(
                whose='id', equals=product.id
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

    @property
    def data(self):
        _data = dict(self.__dict__)
        if not self.has_id():
            _data.pop('id')
        return _data

    def validate_no_id(self):
        if self.has_id():
            raise ValueError("Product can't have an already assigned id")

    def has_id(self):
        return self.id is not None

    def __eq__(self, another_product):
        return self.id == another_product.id
