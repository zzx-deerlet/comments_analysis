# first_demoProject/app/crawler/zhihu_crawler.py
import requests
import re
from fake_useragent import UserAgent
from datetime import datetime

class ZhihuCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": self.ua.random
        }

    def clean_text(self, text):
        """清理 HTML 标签和特殊字符"""
        return re.compile(r'<[^>]+>').sub('', text)

    def get_comments(self, question_id):
        # 这里需要实现知乎评论的爬取逻辑
        # 示例代码，需要根据实际情况修改
        url = f"https://www.zhihu.com/api/v4/questions/{question_id}/answers"
        params = {
            "include": "data[*].content",
            "limit": 20,
            "offset": 0
        }
        response = requests.get(url, params=params, headers=self.headers)
        data = response.json()
        comments = []
        for answer in data.get('data', []):
            comment_data = {
                'platform': '知乎',
                'content': self.clean_text(answer['content']),
                'sentiment': 0,
                'keywords': None,
                'publish_time': datetime.fromtimestamp(answer['created_time']),
                'crawl_time': datetime.now(),
                'confidence': None,
                'reply_count': 0,
                'forward_count': 0,
                'original_id': answer['id'],
                'extra_info': {
                    'author': answer['author']['name']
                }
            }
            comments.append(comment_data)
        return comments