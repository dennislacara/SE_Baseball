import os
from psycopg2.pool import SimpleConnectionPool


class DBConnect:
    _pool_connessioni = None

    def __init__(self):
        raise RuntimeError("Non creare un'istanza, usa get_connection()!")

    @classmethod
    def get_connection(cls, dimensione_pool=3):
        if cls._pool_connessioni is None:
            db_url = os.environ["DATABASE_URL"]

            cls._pool_connessioni = SimpleConnectionPool(
                1,                 # min conn
                dimensione_pool,   # max conn
                db_url
            )

        return cls._pool_connessioni.getconn()

    @classmethod
    def release_connection(cls, conn):
        if cls._pool_connessioni and conn:
            cls._pool_connessioni.putconn(conn)
