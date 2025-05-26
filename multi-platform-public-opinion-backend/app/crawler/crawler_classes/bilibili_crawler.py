import hashlib
import json
import re
from pprint import pprint

import requests
import time
import xml.etree.ElementTree as ET
import pandas as pd
import os
from fake_useragent import UserAgent
from urllib.parse import quote

from app.database.opinion_repository import OpinionRepository
from app.utils.getBV import spider_bvid
from myConfig import webCookies


def trans_date(v_timestamp):
    """10位时间戳转换为时间字符串"""
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def Hash(date, offset, oid, cur_page):
    next_offset = '{"offset":%s}' % offset
    chuli = quote(next_offset)
    if cur_page == 1:
        en = [
            "mode=3",
            f"oid={oid}",
            f"pagination_str={chuli}",
            "plat=1",
            "seek_rpid=",
            "type=1",
            "web_location=1315875",
            f"wts={date}"
        ]
    else:
        en = [
            "mode=3",
            f"oid={oid}",
            f"pagination_str={chuli}",
            "plat=1",
            "type=1",
            "web_location=1315875",
            f"wts={date}"
        ]
    Jt = '&'.join(en)
    sign = 'ea1db124af3c7062474693fa704f4ff8'
    s = Jt + sign
    md5_obj = hashlib.md5()
    s_bytes = s.encode(encoding='utf-8')
    md5_obj.update(s_bytes)
    w_rid = md5_obj.hexdigest()
    return w_rid


class BilibiliCrawler:
    def __init__(self):
        # 这里的UserAgent -> 为随机虚拟的
        self.ua = UserAgent()
        # platform_id -> 数据库platforms表里的b站id
        self.platform_id = 5
        # OpinionRepository_DB -> 初始化一个数据库操作类
        self.OpinionRepository_DB = OpinionRepository()
        # OpinionRepository_DB -> 初始化一个数据库操作类
        self.headers = {
            "User-Agent": self.ua.random,
            "accept": "application/json, text/plain, */*",
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            "If-Modified-Since": "Tue, 141 May 2024 09:00:23 GMT",
            "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "Sec-Ch-Ua-Mobile": '?0',
            'Sec-Ch-Ua-Platform': "Windows",
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            "Cookie": webCookies.BilibiliCookies
        }
        self.dr = re.compile(r'<[^>]+>', re.S)  # 用正则表达式清洗评论数据

        # china_provinces_and_regions -> 用于清洗ip属地
        self.china_provinces_and_regions = [
            "北京市", "天津市", "上海市", "重庆市",
            "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省",
            "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",
            "河南省", "湖北省", "湖南省", "广东省",
            "海南省", "四川省", "贵州省", "云南省", "陕西省", "甘肃省",
            "青海省", "台湾省",
            "内蒙古自治区", "广西壮族自治区", "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区",
            "香港特别行政区", "澳门特别行政区"
        ]

    def get_danmu(self, b_ids, v_bili_file):
        time_list = []  # 弹幕时间
        text_list = []  # 弹幕内容
        for b_id in b_ids:
            url = f" https://www.bilibili.com/video/{b_id}"
            r1 = requests.get(url=url, headers=self.headers)
            print(url)
            print(r1.status_code)
            cid = re.findall('"cid":\s*(\d+)', r1.text)[0]  # 获取视频对应的cid号
            print('该视频的cid是:', cid)

            url = f"https://comment.bilibili.com/{cid}.xml"

            print('弹幕地址是：', url)
            r2 = requests.get(url, headers=self.headers)
            html2 = r2.text.encode('raw unicode escape')

            soup = ET.fromstring(html2)
            danmu_list = soup.findall('d')
            print('共爬取到{}条弹幕'.format(len(danmu_list)))

            for d in danmu_list:
                data_split = d.get('p').split(',')  # 按逗号分隔
                temp_time = int(data_split[4])  # 转换时间格式
                danmu_time = trans_date(temp_time)

                time_list.append(danmu_time)
                text_list.append(d.text)
                print('{}:{}'.format(danmu_time, d.text))

            df = pd.DataFrame(
                {
                    "弹幕内容": text_list,
                    "弹幕时间": time_list
                }
            )

            if os.path.exists(v_bili_file):  # 如果文件存在，不再设置表头
                header = False
            else:  # 否则，设置csv文件表头
                header = True
            # 保存csv文件
            df.to_csv(v_bili_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
            print('结果保存成功:{}'.format(v_bili_file))

    def get_comments(self, b_Bid_list, pages):
        # uname = []  # 用户名
        # rcount = []  # 回复数
        # like = []  # 点赞数
        # sex = []  # 性别
        # comment_list = []  # 评论内容
        # ip_list = []  # IP属地
        # comment_times = []  # 评论时间
        for v_Bid in b_Bid_list:
            oid = self.get_oid(v_Bid)
            offset = '""'
            for page in range(1, pages):
                print(f"==正在爬取第{page}页评论==")
                wts = round(time.time())
                w_rid = Hash(date=wts, offset=offset, oid=oid, cur_page=page)
                if page == 1:
                    params = {
                        "oid": f"{oid}",
                        "type": "1",
                        "mode": "3",
                        "pagination_str": '{"offset":%s}' % offset,
                        "plat": "1",
                        "seek_rpid": "",
                        "web_location": "1315875",
                        "w_rid": f"{w_rid}",
                        "wts": f"{wts}"
                    }
                    r = self.GetRespond("https://api.bilibili.com/x/v2/reply/wbi/main", params)
                    json_text = r.json()
                    # print(json_text)
                    offset = json_text['data']['cursor']['pagination_reply']['next_offset']
                    offset = json.dumps(offset)
                    self.analyze_json(json_text)
                else:
                    params = {
                        "oid": oid,
                        "type": "1",
                        "mode": "3",
                        "pagination_str": '{"offset":%s}' % offset,
                        "plat": "1",
                        "web_location": "1315875",
                        "w_rid": w_rid,
                        "wts": wts
                    }
                    r = self.GetRespond("https://api.bilibili.com/x/v2/reply/wbi/main", params)
                    json_text = r.json()
                    replies = json_text['data']['replies']
                    if not replies:
                        break
                    self.data_save_to_DB(replies)

        # df = pd.DataFrame({
        #     '用户名': uname,
        #     '评论内容': comment_list,
        #     '点赞数': like,
        #     '回复数': rcount,
        #     '性别': sex,
        #     '评论时间': comment_times,
        #     'IP属地': ip_list,
        # })
        #
        # df.to_csv(save_file, mode='w+', index=False, encoding='utf_8_sig')

    def get_oid(self, BV):
        url_for_oid = f" https://www.bilibili.com/video/{BV}"
        r1 = requests.get(url=url_for_oid, headers=self.headers)
        oid = re.findall('"aid":\s*(\d+)', r1.text)[0]  # 获取视频对应的aid号即oid号
        return oid

    def GetRespond(self, url, data):
        r = requests.get(url=url, params=data, headers=self.headers, proxies=webCookies.proxies)
        print(r.status_code)
        # print(r.json())
        return r

    def analyze_json(self, json_text):
        replies = json_text['data']['replies']
        self.data_save_to_DB(replies)

    def data_save_to_DB(self, replies):

        for reply in replies:
            # 定位获取到评论内容
            comment = reply['content']['message']

            # 初步清洗评论内容
            comment = self.dr.sub('', comment)

            # 清洗以后如果为空则直接跳过 不予保存
            if comment == "":
                continue

            # 定位获取到评论的id
            comment_id = reply["rpid"]

            # 定位获取到评论用户的用户名
            comment_uname = reply['member']['uname']

            # 定位获取到评论的时间
            comment_time = trans_date(reply['ctime'])

            # 定位获取到评论的点赞数
            comment_like = reply['like']

            # 定位获取到评论的回复数
            comment_rcount = reply['rcount']

            # 定位获取到评论的回复数
            try:
                # eg: 'IP属地：湖南'
                location = reply['reply_control']['location']
                location = location.replace("IP属地：", "")
                location = location.replace("省", "")

            except:
                location = "未知"

            # 定位获取到评论的回复数
            sex_tag = reply['member']['sex']

            # 如果存在子评论 继续递归获取
            if reply['replies']:
                self.data_save_to_DB(reply['replies'])

            data = {
                "platform_id": self.platform_id,
                "content": comment,
                "publish_time": comment_time,
                "comment_id": comment_id,
                "author": comment_uname,
                "ip": location,
                "gender": sex_tag,
                "like_count": comment_like,
                "reply_count": comment_rcount
            }

            try:
                print("正在储存")
                pprint(data, indent=2)
                self.OpinionRepository_DB.create_one_raw_opinion(data)
            except Exception as e:
                print(f"data_save_to_DB.data_save_to_DB() error:{e}")



# if __name__ == '__main__':
# keyword = "陶喆"

# BV_list = spider_bvid(keyword, 1)

# crawler = BilibiliCrawler()

# # 爬取弹幕
# bili_b_id_list_danmu = \
#     ["BV1t24y1Z7j2"
#      ]
# danmu_file = 'bili_danmu_大学生就业_test.csv'
# crawler.get_danmu(b_ids=bili_b_id_list_danmu, v_bili_file=danmu_file)

# 爬取评论
# bili_b_id_list_comment = \
#     ["BV1Xb421Y7UL"
#      ]
# page = 2  # 爬取的页数
# save_file = "bilibili_comment_大学生就业.csv"
# crawler.get_comments(b_Bid_list=BV_list, pages=page)

# def analyze_json(self, json_text, sex, comment_list, ip_list, comment_times, uname, like, rcount):
#     replies = json_text['data']['replies']
#     self.data_save(replies, sex, comment_list, ip_list, comment_times, uname, like, rcount)
#
# def data_save(self, replies, sex, comment_list, ip_list, comment_times, uname, like, rcount):
#     for reply in replies:
#         comment = reply['content']['message']
#         comment = self.dr.sub('', comment)
#         if comment == "":
#             continue
#         comment_list.append(comment)  # 列表中加入一条评论内容
#
#         comment_uname = reply['member']['uname']
#         uname.append(comment_uname)  # 列表中加入一个用户名
#
#         comment_time = trans_date(reply['ctime'])
#         comment_times.append(comment_time)  # 加入评论时间
#
#         comment_like = reply['like']
#         like.append(comment_like)  # 加入点赞数
#
#         comment_rcount = reply['rcount']
#         rcount.append(comment_rcount)  # 加入回复数
#         try:
#             ip_list.append(reply['reply_control']['location'])
#         except:
#             ip_list.append("未知")
#
#         sex_tag = reply['member']['sex']
#         sex.append(sex_tag)
#         # 如果存在子评论
#         if reply['replies']:
#             self.data_save(reply['replies'], sex, comment_list, ip_list, comment_times, uname, like, rcount)

# todo 异步处理
