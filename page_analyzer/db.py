import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv
from datetime import datetime
from psycopg2.extras import RealDictCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


@contextmanager
def launch_connection():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        yield connection
    finally:
        if connection:
            connection.close()


def connection_db(cursor_factory=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with launch_connection() as connection:
                with connection.cursor(cursor_factory=cursor_factory) as cursor:
                    return func(connection, cursor, *args, **kwargs)
        return wrapper
    return decorator


@connection_db(cursor_factory=None)
def save_url_db(connection, cursor, url_data):
    cursor.execute(
        'INSERT INTO urls(name, created_at)\
        VALUES(%s, %s) RETURNING id;',
        (
            url_data.get('name'),
            str(datetime.now())
        )
    )
    record = cursor.fetchone()
    connection.commit()
    return record[0]


@connection_db(cursor_factory=None)
def delete_url_db(connection, cursor, url_id):
    cursor.execute('DELETE FROM urls WHERE id=%s;', (url_id,))
    connection.commit()


@connection_db(cursor_factory=RealDictCursor)
def find_all_urls_db(connection, cursor, limit=10):
    cursor.execute(
        'SELECT\
        urls.name, ch.status_code, ch.url_id, ch.created_at\
        FROM urls\
        JOIN url_checks as ch\
        ON ch.url_id = urls.id\
        AND ch.created_at IN (SELECT MAX(created_at)\
        FROM url_checks GROUP BY url_id)\
        ORDER BY url_id DESC\
        LIMIT %s;',
        (limit,)
    )
    return cursor.fetchall()


@connection_db(cursor_factory=RealDictCursor)
def find_url_id(connection, cursor, url_id):
    cursor.execute(
        'SELECT * FROM urls WHERE id = %s;',
        (url_id,),
    )
    return cursor.fetchone()


@connection_db(cursor_factory=RealDictCursor)
def find_url_name(connection, cursor, url_name):
    cursor.execute(
        'SELECT * FROM urls WHERE name = %s;',
        (url_name,),
    )
    return cursor.fetchone()


@connection_db(cursor_factory=None)
def save_check(connection, cursor, url_id, check_data):
    cursor.execute(
        'INSERT INTO url_checks\
        (url_id, status_code, h1, title, description, created_at)\
        VALUES(%s, %s, %s, %s, %s, %s);',
        (
            url_id,
            check_data.get('status_code', ''),
            check_data.get('h1', ''),
            check_data.get('title', ''),
            check_data.get('meta', ''),
            str(datetime.now()),
        ),
    )
    connection.commit()


@connection_db(cursor_factory=RealDictCursor)
def find_all_checks(connection, cursor, url_id):
    cursor.execute(
        'SELECT * FROM url_checks WHERE url_id=%s\
        ORDER BY created_at DESC;',
        (url_id,)
    )
    return cursor.fetchall()
