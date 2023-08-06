import logging
import sys
import uuid

from django.conf import settings
from django.db import connection

logger = logging.getLogger(__name__)


def create_tmp_mat_view(sql_str, params=[], indexes=[], mat_view_name=None):
    if mat_view_name != None:
        settings.LOCKS.acquire(f'create_tmp_mat_view_{mat_view_name}')
    else:
        mat_view_name = f'tmp_{str(uuid.uuid4()).replace("-", "_")}'


    if isinstance(indexes, list):
        indexes = [f'CREATE INDEX {mat_view_name}_{index}_idx ON {mat_view_name} USING btree ({index})' for index in indexes]
        suffix = ';'.join(indexes)
    sql_txt = f'''CREATE MATERIALIZED VIEW {mat_view_name} AS {sql_str} WITH DATA; {suffix}'''
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_txt, params)
        if mat_view_name != None:
            settings.LOCKS.release(f'create_tmp_mat_view_{mat_view_name}')
        return mat_view_name
    except Exception as ex:
        exc_info = sys.exc_info()
        logger.error(msg=ex, exc_info=exc_info)
        if mat_view_name != None:
            settings.LOCKS.release(f'create_tmp_mat_view_{mat_view_name}')
        return None


def drop_mat_view(mat_view_name):
    sql_txt = f'DROP MATERIALIZED VIEW IF EXISTS {mat_view_name} CASCADE;'
    try:
        settings.LOCKS.acquire(f'drop_mat_view_{mat_view_name}')
        with connection.cursor() as cursor:
            cursor.execute(sql_txt)
        settings.LOCKS.release(f'drop_mat_view_{mat_view_name}')
        return True
    except Exception as ex:
        exc_info = sys.exc_info()
        logger.error(msg=ex, exc_info=exc_info)
        settings.LOCKS.release(f'drop_mat_view_{mat_view_name}')
        return False


def refresh_mat_view(mat_view_name):
    sql_txt = f'REFRESH MATERIALIZED VIEW {mat_view_name};'
    settings.LOCKS.acquire(f'refresh_mat_view_{mat_view_name}')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_txt)
        settings.LOCKS.release(f'refresh_mat_view_{mat_view_name}')
        return True
    except Exception as ex:
        exc_info = sys.exc_info()
        logger.error(msg=ex, exc_info=exc_info)
        settings.LOCKS.release(f'refresh_mat_view_{mat_view_name}')
        return False
