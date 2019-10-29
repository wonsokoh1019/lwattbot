import psycopg2
import psycopg2.extras as extras
from psycopg2.errors import DuplicateTable
from DBUtils.PooledDB import PooledDB
from DBUtils.PersistentDB import PersistentDB
from calender.constant import DB_CONFIG


class PostGreSql:
    __pool = None

    def __init__(self):
        self.conn = PostGreSql.__get_conn()
        self.cursor = self.conn.cursor()

    @staticmethod
    def __get_conn():
        if PostGreSql.__pool is None:
            __pool = PooledDB(creator=psycopg2, mincached=1, maxcached=20,
                              host=DB_CONFIG["host"],
                              port=DB_CONFIG["port"],
                              user=DB_CONFIG["user"],
                              password=DB_CONFIG["password"],
                              database=DB_CONFIG["name"],
                              sslmode=DB_CONFIG["ssl"])
        return __pool.connection()

    def close(self):
        self.cursor.close()
        self.conn.close()
