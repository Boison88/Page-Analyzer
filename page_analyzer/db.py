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


def save(url_data):
    with launch_connection() as connection:
        with connection.cursor() as cursor:
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


def delete(url_id):
    with launch_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM urls WHERE id=%s;', (url_id,))
            connection.commit()


def find_all(limit=10):
    with launch_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
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


def find_url_id(url_id):
    with launch_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                'SELECT * FROM urls WHERE id = %s;',
                (url_id,),
            )
            return cursor.fetchone()


def find_url_name(url_name):
    with launch_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                'SELECT * FROM urls WHERE name = %s;',
                (url_name,),
            )
            return cursor.fetchone()


def save_check(url_id, check_data):
    with launch_connection() as connection:
        with connection.cursor() as cursor:
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


def find_all_checks(url_id):
    with launch_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                'SELECT * FROM url_checks WHERE url_id=%s\
                ORDER BY created_at DESC;',
                (url_id,)
            )
            return cursor.fetchall()
