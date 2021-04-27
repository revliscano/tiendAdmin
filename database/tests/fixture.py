from database.sqlalchemy_data_layer import data_access_layer


def populate_database_with_products():
    product_table = data_access_layer.product
    data_access_layer.connection.execute(
        product_table.insert(),
        name='Existing Product',
        price=100
    )
    data_access_layer.connection.execute(
        product_table.insert(),
        name='Duplicated Product',
        price=200
    )
    data_access_layer.connection.execute(
        product_table.insert(),
        name='Duplicated Product',
        price=200
    )


def clear_table():
    table = data_access_layer.product
    data_access_layer.connection.execute(
        table.delete()
    )
