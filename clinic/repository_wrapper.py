import pymysql
from pymysql.cursors import DictCursor
from repository import RepositoryManager
from django.conf import settings

_conn = None
_repos = None

def get_connection():
    global _conn
    if _conn is None:
        cfg = {
            'host': settings.MYSQL_HOST,
            'user': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWORD,
            'database': settings.MYSQL_DB,
            'cursorclass': DictCursor,
            'autocommit': False,
        }
        _conn = pymysql.connect(**cfg)
    return _conn

def get_repos():
    global _repos
    if _repos is None:
        conn = get_connection()
        _repos = RepositoryManager(conn)
    return _repos

def commit():
    conn = get_connection()
    conn.commit()

def rollback():
    conn = get_connection()
    conn.rollback()