import pymysql
from myConfig import dbConfig


def init_database():
    config = dbConfig()

    # 连接到MySQL服务器（不指定数据库）
    conn = pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD
    )

    try:
        # 创建数据库（如果不存在）
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DB} CHARACTER SET utf8mb4")

        # 连接到指定数据库
        conn.select_db(config.MYSQL_DB)

        # 创建表
        with conn.cursor() as cursor:

            # 创建platforms表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS platforms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(20) UNIQUE NOT NULL COMMENT '平台名称',
                base_url VARCHAR(255) COMMENT '平台基础URL',
                is_active TINYINT DEFAULT 1 COMMENT '是否启用',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # 创建raw_public_opinion表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_public_opinion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                platform_id INT NOT NULL COMMENT '平台ID，关联platforms表的id',
                content TEXT NOT NULL COMMENT '评论内容',
                publish_time DATETIME NOT NULL COMMENT '发布时间',
                crawl_time DATETIME NOT NULL COMMENT '爬取时间',
                comment_id VARCHAR(50) COMMENT '原评论ID',
                author VARCHAR(255) COMMENT '评论作者',
                ip VARCHAR(255) COMMENT '评论者IP属地',
                gender VARCHAR(10) COMMENT '评论者性别',
                like_count INT DEFAULT 0 COMMENT '点赞数',
                reply_count INT DEFAULT 0 COMMENT '回复数',
                FOREIGN KEY (platform_id) REFERENCES platforms(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # 创建analyzed_public_opinion表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyzed_public_opinion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                raw_opinion_id INT NOT NULL COMMENT '关联raw_public_opinion表的id',
                sentiment TINYINT DEFAULT 0 COMMENT '-1=负面, 0=中性, 1=正面',
                keywords TEXT COMMENT '关键词',
                confidence DECIMAL(5,2) COMMENT '情感分析置信度',
                reply_count INT DEFAULT 0 COMMENT '回复数',
                forward_count INT DEFAULT 0 COMMENT '转发数',
                FOREIGN KEY (raw_opinion_id) REFERENCES raw_public_opinion(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # 创建users表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL, 
                password_hash VARCHAR(255) NOT NULL,   
                role ENUM('admin', 'user') DEFAULT 'user',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # 为 comment_id 和 platform_id 字段添加索引
            cursor.execute("""
            CREATE INDEX idx_platform_id ON raw_public_opinion (platform_id);
            """)

            cursor.execute("""
            ALTER TABLE raw_public_opinion ADD UNIQUE (comment_id);
            """)

        print("数据库初始化完成！")

    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
