import pymysql
from myConfig import dbConfig


class Database:
    def __init__(self):
        self.config = dbConfig()

    def get_connection(self):
        """获取数据库连接"""
        # print("正在获取连接...")

        return pymysql.connect(
            host=self.config.MYSQL_HOST,
            user=self.config.MYSQL_USER,
            password=self.config.MYSQL_PASSWORD,
            database=self.config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True  # 启用自动提交
        )
