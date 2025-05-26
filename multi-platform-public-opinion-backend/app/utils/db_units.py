import pymysql
import myConfig

class Database:
    def __init__(self):
        self.config = myConfig.dbConfig

    def get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(
            host=self.config.MYSQL_HOST,
            user=self.config.MYSQL_USER,
            password=self.config.MYSQL_PASSWORD,
            database=self.config.MYSQL_DB,
            charset='utf8mb4',
            # cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, query, params=None):
        """执行SQL语句"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid

    def query(self, query, params=None):
        """查询数据"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()