from database.sqlalchemy_data_layer import data_access_layer


def populate_database_with_products():
    product_table = data_access_layer.product
    data_access_layer.connection.execute(
        product_table.insert(),
        name='Existing Product',
        price=1000
    )
