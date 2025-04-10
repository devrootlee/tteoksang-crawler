import os

import psycopg2

def db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=5432,
        dbname=os.environ.get("DB"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD")
    )