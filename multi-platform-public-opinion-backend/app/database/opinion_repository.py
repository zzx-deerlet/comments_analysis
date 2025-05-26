from .connection import Database
from datetime import datetime


class OpinionRepository:
    def __init__(self):
        self.db = Database()

    def create_one_raw_opinion(self, data):
        """新增一条原始舆情数据"""
        query = """
        INSERT INTO raw_public_opinion 
        (platform_id, content, publish_time, crawl_time, comment_id, author, ip, gender, like_count, reply_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data['platform_id'],
            data['content'],
            data['publish_time'],
            datetime.now(),  # 自动记录爬取时间
            data.get('comment_id'),
            data.get('author'),
            data.get('ip'),
            data.get('gender'),
            data.get('like_count', 0),
            data.get('reply_count', 0)
        )

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.lastrowid

    def create_raw_opinions(self, data_list):
        """新增列表里所有原始舆情数据"""
        query = """
           INSERT INTO raw_public_opinion 
           (platform_id, content, publish_time, crawl_time, comment_id, author, ip, gender, like_count, reply_count)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """
        params = []
        for data in data_list:
            param = (
                data['platform_id'],
                data['content'],
                data['publish_time'],
                datetime.now(),  # 自动记录爬取时间
                data.get('comment_id'),
                data.get('author'),
                data.get('ip'),
                data.get('gender'),
                data.get('like_count', 0),
                data.get('reply_count', 0)
            )
            params.append(param)

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, params)
                return cursor.rowcount


    def create_analyzed_opinion(self, data):
        """新增分析后的舆情数据"""
        query = """
        INSERT INTO analyzed_public_opinion 
        (raw_opinion_id, sentiment, keywords, confidence, reply_count, forward_count)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data['raw_opinion_id'],
            data.get('sentiment', 0),
            data.get('keywords'),
            data.get('confidence'),
            data.get('reply_count', 0),
            data.get('forward_count', 0)
        )

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.lastrowid

    def get_raw_opinion_by_id(self, opinion_id):
        """根据ID查询原始舆情数据"""
        query = """
        SELECT rp.*, p.name as platform_name 
        FROM raw_public_opinion rp
        JOIN platforms p ON rp.platform_id = p.id
        WHERE rp.id = %s
        """

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (opinion_id,))
                return cursor.fetchone()

    def get_analyzed_opinion_by_id(self, opinion_id):
        """根据ID查询分析后的舆情数据"""
        query = """
        SELECT ap.*, rp.content, rp.author, rp.platform_id, p.name as platform_name
        FROM analyzed_public_opinion ap
        JOIN raw_public_opinion rp ON ap.raw_opinion_id = rp.id
        JOIN platforms p ON rp.platform_id = p.id
        WHERE ap.id = %s
        """

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (opinion_id,))
                return cursor.fetchone()

    def get_raw_opinion_list(self, platform_id=None, limit=100, offset=0):
        """查询原始舆情数据列表"""
        query = """
        SELECT rp.*, p.name as platform_name
        FROM raw_public_opinion rp
        JOIN platforms p ON rp.platform_id = p.id
        WHERE 1=1
        """
        params = []

        if platform_id:
            query += " AND rp.platform_id = %s"
            params.append(platform_id)

        query += " ORDER BY rp.publish_time DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

    def get_analyzed_opinion_list(self, platform_id=None, sentiment=None, limit=100, offset=0):
        """查询分析后的舆情数据列表"""
        query = """
        SELECT ap.*, rp.content, rp.author, rp.platform_id, p.name as platform_name
        FROM analyzed_public_opinion ap
        JOIN raw_public_opinion rp ON ap.raw_opinion_id = rp.id
        JOIN platforms p ON rp.platform_id = p.id
        WHERE 1=1
        """
        params = []

        if platform_id:
            query += " AND rp.platform_id = %s"
            params.append(platform_id)

        if sentiment is not None:
            query += " AND ap.sentiment = %s"
            params.append(sentiment)

        query += " ORDER BY ap.id DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

    def update_raw_opinion(self, opinion_id, data):
        """更新原始舆情数据"""
        set_clauses = []
        params = []

        for key, value in data.items():
            if key != 'id':  # 防止更新ID
                set_clauses.append(f"{key} = %s")
                params.append(value)

        params.append(opinion_id)
        query = f"UPDATE raw_public_opinion SET {', '.join(set_clauses)} WHERE id = %s"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount

    def update_analyzed_opinion(self, opinion_id, data):
        """更新分析后的舆情数据"""
        set_clauses = []
        params = []

        for key, value in data.items():
            if key != 'id':  # 防止更新ID
                set_clauses.append(f"{key} = %s")
                params.append(value)

        params.append(opinion_id)
        query = f"UPDATE analyzed_public_opinion SET {', '.join(set_clauses)} WHERE id = %s"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount

    def delete_raw_opinion(self, opinion_id):
        """删除原始舆情数据"""
        query = "DELETE FROM raw_public_opinion WHERE id = %s"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (opinion_id,))
                return cursor.rowcount

    def delete_analyzed_opinion(self, opinion_id):
        """删除分析后的舆情数据"""
        query = "DELETE FROM analyzed_public_opinion WHERE id = %s"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (opinion_id,))
                return cursor.rowcount

    def count_raw_opinions_by_platform(self):
        """统计各平台原始舆情数量"""
        query = """
        SELECT p.name, COUNT(*) as count 
        FROM raw_public_opinion rp
        JOIN platforms p ON rp.platform_id = p.id
        GROUP BY p.name
        """

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def count_analyzed_opinions_by_sentiment(self, platform_id=None):
        """统计分析后的舆情情感分析结果"""
        query = """
        SELECT ap.sentiment, COUNT(*) as count 
        FROM analyzed_public_opinion ap
        JOIN raw_public_opinion rp ON ap.raw_opinion_id = rp.id
        JOIN platforms p ON rp.platform_id = p.id
        """

        params = []
        if platform_id:
            query += " WHERE rp.platform_id = %s"
            params.append(platform_id)

        query += " GROUP BY ap.sentiment"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

    def get_top_liked_comments(self, limit=10):
        """获取点赞数最高的评论"""
        query = """
        SELECT rp.*, p.name as platform_name
        FROM raw_public_opinion rp
        JOIN platforms p ON rp.platform_id = p.id
        ORDER BY rp.like_count DESC
        LIMIT %s
        """

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (limit,))
                return cursor.fetchall()

    def get_top_replied_comments(self, limit=10):
        """获取回复数最高的评论"""
        query = """
        SELECT rp.*, p.name as platform_name
        FROM raw_public_opinion rp
        JOIN platforms p ON rp.platform_id = p.id
        ORDER BY rp.reply_count DESC
        LIMIT %s
        """

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (limit,))
                return cursor.fetchall()