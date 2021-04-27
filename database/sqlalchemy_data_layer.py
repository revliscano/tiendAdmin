from sqlalchemy import (
    MetaData, Table, Column, Integer, String,
    Boolean, create_engine
)


class DataAccessLayer:
    connection = None
    engine = None
    conn_string = None
    metadata = MetaData()

    product = Table(
        'product',
        metadata,
        Column('id', Integer(), primary_key=True, unique=True),
        Column('name', String(100)),
        Column('quantity', Integer(), default=0),
        Column('price', Integer(), default=0),
        Column('is_fixed_to_USD', Boolean(), default=True)
    )

    def db_init(self, conn_string):
        self.engine = create_engine(conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

    def close_connection(self):
        self.connection.close()

    def get_latest_inserted_ids(self, result):
        insertions = result.rowcount
        raw_connection = self.engine.raw_connection()
        cursor = raw_connection.cursor()
        last_inserted_id, = cursor.execute(
            'SELECT last_insert_rowid()'
        ).fetchone()
        return tuple(
            range(last_inserted_id - insertions + 1, last_inserted_id + 1)
        )


data_access_layer = DataAccessLayer()
