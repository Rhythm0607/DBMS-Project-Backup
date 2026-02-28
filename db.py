import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Please configure it in your .env file."
    )


def get_connection():
    """
    Create and return a new database connection.
    Uses RealDictCursor so rows behave like dicts: row['column_name'].
    """
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


@contextmanager
def get_cursor(commit: bool = False):
    """
    Convenience context manager for DB operations.

    Example:
        with get_cursor(commit=True) as cur:
            cur.execute("UPDATE ...", params)
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_one(sql: str, params: dict | tuple | None = None):
    with get_cursor() as cur:
        cur.execute(sql, params or {})
        return cur.fetchone()


def fetch_all(sql: str, params: dict | tuple | None = None):
    with get_cursor() as cur:
        cur.execute(sql, params or {})
        return cur.fetchall()


def execute(sql: str, params: dict | tuple | None = None):
    with get_cursor(commit=True) as cur:
        cur.execute(sql, params or {})

