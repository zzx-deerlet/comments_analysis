import re
import requests
import time
import os
import random
from fake_useragent import UserAgent
import datetime

class ToutiaoCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": self.ua.random,
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "Cookie": """ttwid=1%7C0f6Go2o323F0zj2SKQUgssUIh5u61el1tM4TBmklvWw%7C1745281730%7C3330ce2139e3601dcaac083063fb1c3d43aa3e06214b29dc4470186330d26d05"""
        }

    @staticmethod
    def trans_date(timestamp):
        """10位时间戳转换为时间字符串"""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    def clean_text(self, text):
        """清理HTML标签和特殊字符"""
        return re.compile(r'<[^>]+>').sub('', text)

    def get_comments(self, answer_ids, max_page=10):
        all_comments = []
        for answer_id in answer_ids:
            for page in range(0, max_page * 20, 20):
                print(f"正在爬取回答{answer_id}的第{(page // 20) + 1}页评论")
                url = f"https://www.toutiao.com/article/v4/tab_comments/?aid=24&group_id={answer_id}&offset={page}"

                try:
                    response = requests.get(url, headers=self.headers)
                    response.raise_for_status()
                    data = response.json()

                    comments = data.get('data', [])
                    if not comments:
                        break

                    for comment in comments:
                        comment_data = {
                            'id': comment['comment']['id'],
                            'content': self.clean_text(comment['comment']['text']),
                            'author': comment['comment']['user_name'],
                            'ip': comment['comment']['publish_loc_info'],
                            'publish_time': self.trans_date(comment['comment']['create_time']),
                            'page': (page // 20) + 1,
                            'extra_info': {
                                'answer_id': answer_id
                            }
                        }
                        all_comments.append(comment_data)

                except Exception as e:
                    print(f"爬取第{(page // 20) + 1}页时出错: {e}")
                    continue

        return all_comments