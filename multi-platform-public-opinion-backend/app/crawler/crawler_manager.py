import os
import pandas as pd
import datetime
from app.database.opinion_repository import OpinionRepository
from .crawler_classes.bilibili_crawler import BilibiliCrawler
from ..utils.getBV import spider_bvid


class CrawlerManager:
    def __init__(self):
        self.opinion_repo = OpinionRepository()
        self.bilibili_comment_crawler = BilibiliCrawler()

    def getDataByKeyWord_Bilibili(self, video_keyword, video_page, comment_page):
        """整合B站通过搜索关键词获取视频BV列表以及爬取评论功能"""
        BV_list = spider_bvid(video_keyword, video_page)
        self.bilibili_comment_crawler.get_comments(b_Bid_list=BV_list, pages=comment_page)

    def getDataByKeyWord_TieBa(self, video_keyword, video_page, comment_page):
        """整合贴吧通过搜索关键词获取视频BV列表以及爬取评论功能"""
        BV_list = spider_bvid(video_keyword, video_page)

    def getDataByKeyWord_WeiBo(self, video_keyword, video_page, comment_page):
        """整合B站通过搜索关键词获取视频BV列表以及爬取评论功能"""
        BV_list = spider_bvid(video_keyword, video_page)

    def getDataByKeyWord_ZhiHu(self, video_keyword, video_page, comment_page):
        """整合B站通过搜索关键词获取视频BV列表以及爬取评论功能"""
        BV_list = spider_bvid(video_keyword, video_page)

    def run_all(self, video_keyword):
        """运行所有爬虫"""
        self.getDataByKeyWord_Bilibili(video_keyword=video_keyword, video_page=10, comment_page=10)
