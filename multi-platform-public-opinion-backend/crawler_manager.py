import os
import pandas as pd
import datetime
from .jinritoutiao import ToutiaoCrawler
from .weibo.weibo_pinglun import get_comments as weibo_get_comments
from .tieba.tieba_pinglun import TiebaCrawler  # 假设 tieba_pinglun.py 中有 TiebaCrawler 类
from .知乎.zhihu_pinglun import ZhihuCrawler  # 假设 zhihu_pinglun.py 中有 ZhihuCrawler 类
from .bilibili.danmu import DanmuCrawler  # 假设 danmu 目录下有 DanmuCrawler 类
from .bilibili.comments import CommentCrawler  # 假设 comments 目录下有 CommentCrawler 类
from app.database.opinion_repository import OpinionRepository

class CrawlerManager:
    def __init__(self):
        self.opinion_repo = OpinionRepository()
        self.toutiao_crawler = ToutiaoCrawler()
        self.tieba_crawler = TiebaCrawler()
        self.zhihu_crawler = ZhihuCrawler()
        self.bilibili_danmu_crawler = DanmuCrawler()
        self.bilibili_comment_crawler = CommentCrawler()

    def save_to_db(self, platform, data_list):
        """将数据保存到数据库"""
        for data in data_list:
            try:
                opinion = {
                    "platform": platform,
                    "content": data['content'],
                    "sentiment": 0,
                    "keywords": None,
                    "publish_time": data['publish_time'],
                    "crawl_time": datetime.datetime.now(),
                    "confidence": None,
                    "reply_count": 0,
                    "forward_count": 0,
                    "original_id": data['id'],
                    "extra_info": data.get('extra_info', {})
                }
                self.opinion_repo.create(opinion)
            except Exception as e:
                print(f"保存数据到数据库时出错: {e}")

    def crawl_toutiao(self, answer_ids, max_page=10):
        """爬取今日头条评论"""
        comments = self.toutiao_crawler.get_comments(answer_ids, max_page)
        self.save_to_db("今日头条", comments)
        print(f'今日头条评论爬取完成，共 {len(comments)} 条')

    def crawl_weibo(self, weibo_ids, max_page=20):
        """爬取微博评论"""
        id_list = []
        page_list = []
        text_list = []
        time_list = []
        source_list = []
        user_gender_list = []

        weibo_get_comments(weibo_ids, "", max_page)

        data_list = []
        for i in range(len(id_list)):
            data = {
                'id': id_list[i],
                'content': text_list[i],
                'publish_time': time_list[i],
                'extra_info': {
                    '评论页码': page_list[i],
                    '评论者IP归属地': source_list[i],
                    '评论者性别': user_gender_list[i]
                }
            }
            data_list.append(data)

        self.save_to_db("微博", data_list)
        print(f'微博评论爬取完成，共 {len(data_list)} 条')

    def crawl_tieba(self, tieba_urls, max_page=20):
        """爬取贴吧评论"""
        comments = self.tieba_crawler.get_comments(tieba_urls, max_page)
        self.save_to_db("贴吧", comments)
        print(f'贴吧评论爬取完成，共 {len(comments)} 条')

    def crawl_zhihu(self, question_ids, max_page=10):
        """爬取知乎评论"""
        comments = self.zhihu_crawler.get_comments(question_ids, max_page)
        self.save_to_db("知乎", comments)
        print(f'知乎评论爬取完成，共 {len(comments)} 条')

    def crawl_bilibili_danmu(self, bvid):
        """爬取B站弹幕"""
        danmu = self.bilibili_danmu_crawler.get_danmaku(bvid)
        self.save_to_db("B站弹幕", danmu)
        print(f'{bvid} 的B站弹幕爬取完成，共 {len(danmu)} 条')

    def crawl_bilibili_comments(self, bvid, max_page=10):
        """爬取B站评论"""
        comments = self.bilibili_comment_crawler.get_comments(bvid, max_page)
        self.save_to_db("B站评论", comments)
        print(f'{bvid} 的B站评论爬取完成，共 {len(comments)} 条')

    def run_all(self, toutiao_answer_ids, weibo_ids, tieba_urls, zhihu_question_ids, bilibili_bvids):
        """运行所有爬虫"""
        self.crawl_toutiao(toutiao_answer_ids)
        self.crawl_weibo(weibo_ids)
        self.crawl_tieba(tieba_urls)
        self.crawl_zhihu(zhihu_question_ids)
        for bvid in bilibili_bvids:
            self.crawl_bilibili_danmu(bvid)
            self.crawl_bilibili_comments(bvid)