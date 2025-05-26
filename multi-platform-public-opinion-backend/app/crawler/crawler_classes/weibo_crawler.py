import os
import random
import re
from time import sleep
from jsonpath import jsonpath
import requests
import pandas as pd
import datetime
from fake_useragent import UserAgent

class WeiboCrawler:
    def __init__(self):
        self.id_list = []
        self.page_list = []
        self.text_list = []
        self.time_list = []
        self.source_list = []
        self.user_gender_list = []
        self.ua = UserAgent()

    def trans_gender(self, gender_tag):
        if gender_tag == 'm':
            return '男'
        elif gender_tag == 'f':
            return '女'
        else:
            return '未知'

    def trans_time(self, v_str):
        GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
        timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
        return timeArray.strftime("%Y-%m-%d %H:%M:%S")

    def get_comments(self, v_weibo_ids, v_weibo_page):
        all_comments = []
        for weibo_id in v_weibo_ids:
            max_id = '0'
            max_id_type = 0
            error_times = 0
            for page in range(1, v_weibo_page + 1):
                if error_times >= 2:
                    break
                wait_seconds = random.uniform(0, 1)
                sleep(wait_seconds)
                if page == 1:
                    url = f'https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0'
                else:
                    if max_id == '0':
                        break
                    url = f'https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id={max_id}&max_id_type={max_id_type}'
                headers = {
                    "User-Agent": self.ua.random,
                    "accept-encoding": "gzip, deflate, br",
                    "Cookie": """_T_WM=75994909120; XSRF-TOKEN=b531e7; WEIBOCN_FROM=1110006030; mweibo_short_token=e5a13fb68a; MLOGIN=0; M_WEIBOCN_PARAMS=oid%3D5157625814062162%26lfid%3D102803%26luicode%3D20000174""",
                    "Mweibo-Pwa": "1",
                }
                r = requests.get(url=url, headers=headers)
                try:
                    weibo_json = r.json()
                    max_id = weibo_json['data']['max_id']
                    datas = weibo_json['data']['data']
                except Exception as e:
                    max_id_type += 1
                    v_weibo_page += 1
                    error_times += 1
                    continue
                dr = re.compile(r'<[^>]+>', re.S)
                if datas[0]['id'] in self.id_list:
                    break
                for data in datas:
                    comment_data = {
                        'id': data['id'],
                        'content': dr.sub('', data['text']),
                        'publish_time': self.trans_time(data['created_at']),
                        'extra_info': {
                            '评论页码': page,
                            '评论者IP归属地': data['source'],
                            '评论者性别': self.trans_gender(data['user']['gender'])
                        }
                    }
                    all_comments.append(comment_data)
        return all_comments