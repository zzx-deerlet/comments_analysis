# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的环境变量


class dbConfig:
    # 数据库配置
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "zzx2004a")
    MYSQL_DB = os.getenv("MYSQL_DB", "opinion_analysis")


class webCookies:
    BilibiliCookies = """buvid3=6580F070-3553-12E7-DBF5-6E6420F6F8BF15600infoc; b_nut=100; _uuid=C2F24AE2-A433-D6C10-B6ED-8C7529211BA412570infoc; buvid_fp=04445240a9407edff5e629f0ce7f1647; buvid4=A83E4D55-34AE-849F-4B53-6B5FA0A3EB0713959-024120816-C%2FTJfj%2FDCHz1vgPaz24ijw%3D%3D; rpdid=|(k|k)RR|)uR0J'u~JJY~lkul; DedeUserID=1745878425; DedeUserID__ckMd5=5bfc93b536146f6e; header_theme_version=CLOSE; enable_web_push=DISABLE; enable_feed_channel=ENABLE; home_feed_column=5; b_lsid=E6842A55_196FBC5B913; SESSDATA=c386e279%2C1763532767%2C1bba7%2A51CjDKEeXJ7OeMPaWyvaukH6kfBokXHNnLCSJ3JSNWwKScwoilxq76dqARcePbP333uTQSVmFpZTI0QzNjLTByYUdKOWthYm8ydHBvSThUVUhIN09RY0M3bGM1WFY0V1FDRlZkNDUwckFFajlxX05JZGNhTlNpLUU3QlF4Ymk5Wnl5QXFSNkkzTkdBIIEC; bili_jct=5fa6d6cd2f8dea7b39a4255f51b453bb; sid=8n0ik983; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDgyMzk5ODYsImlhdCI6MTc0Nzk4MDcyNiwicGx0IjotMX0.s5KAAHXMu-4HVrEpg6BqL4QBmpCH8VhVdW6cJprCZ_s; bili_ticket_expires=1748239926; browser_resolution=2560-1271; CURRENT_FNVAL=4048; bp_t_offset_1745878425=1070059417824657408"""
    TieBaCookies = """"""
    TouTiaoCookies = """"""
    ZhiHuCookies = """"""
    WeiBoCookies = """"""
    proxies = {"http": "202.101.213.160"}


class BaiDuYunConfig:
    API_KEY = "OxiLWYUBKK6rd4Psf1oDS11T"
    SECRET_KEY = "C1LCYI2qfRU6IA5eJcfjRYDUQrXLta8g"


class LSTMConfig:
    # 训练时批处理次数
    BATCH_SIZE = 32

    # 构建词汇表时的表大小
    max_vocab_size = 15000

    # 每次读入的句子最长长度
    MAX_LEN = 100

    # 训练时的学习率
    LEARNING_RATE = 0.01

    # 训练时的次数
    NUM_EPOCHS = 20
