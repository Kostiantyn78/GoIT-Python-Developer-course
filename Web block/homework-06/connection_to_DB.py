from psycopg2 import connect, Error
from contextlib import contextmanager


# create a connection to the Postgres database
@contextmanager
def create_connection():
    conn = None
    try:
        conn = connect(host='localhost', user='postgres', database='homework_DB', password='1111')
        yield conn
        conn.commit()
    except Error as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
